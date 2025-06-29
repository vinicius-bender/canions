#imports
from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Specialist, Scientist, Family, Genus, Species, Observation, Localization, Media, ObservationMedia
from .forms import FamilyForm, GenusForm, SpeciesForm, LocalizationForm, CustomLoginForm, CustomUserCreationForm, MediaForm, MultipleFileInput, ObservationLatLngForm, ObservationCityForm, AprovarObservacaoForm, ObservationReviewForm, CriarContaRealForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from django.contrib.auth import login
import uuid
from django.http import Http404, HttpResponseNotFound
from django.db.models import F

#views
def is_specialist_or_scientist(user):
    return user.role in ['specialist', 'scientist']

def is_specialist_or_scientist_admin(user):
    return user.role in ['specialist', 'scientist', 'admin']

def is_admin(user):
    return user.is_authenticated and user.role == "admin"

def home(request):

    # Número de espécies
    num_species = Species.objects.filter().distinct().count()

    # Total de registros (todas as observações, independente do status)
    num_records = Observation.objects.count()

    # Total de observações aprovadas
    num_approved_observations = Observation.objects.filter(status='Aprovada').count()

     # Observações aprovadas para o mapa
    observations = Observation.objects.filter(status='Aprovada').select_related('species', 'localization').values(
        'id',
        'latitude',
        'longitude',
        species_name=F('species__popular_name'),
        city=F('localization__city_name'),
        state=F('localization__state_name'),
    )

    context = {
        'user': request.user,
        'num_species': num_species,
        'num_records': num_records,
        'num_approved_observations': num_approved_observations,
        'observations_json': json.dumps(list(observations), cls=DjangoJSONEncoder),
    }

    return render(request, 'canionsDoSul_app/home.html', context)


def about(request):
    return render(request, "canionsDoSul_app/sobre.html")

def contact(request):
    return render(request, "canionsDoSul_app/contato.html")

@login_required
@user_passes_test(is_admin, login_url='erro_permissao')
def admin_panel(request):
    return render(request, 'canionsDoSul_app/painel_administrador.html')

class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = 'canionsDoSul_app/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'canionsDoSul_app/registrar.html', {'form': form})

User = get_user_model()

def get_or_create_anonymous_user(request):
    if request.user.is_authenticated:
        return request.user

    if 'anon_user_id' in request.session:
        try:
            return User.objects.get(id=request.session['anon_user_id'])
        except User.DoesNotExist:
            pass  # Usuário expirou ou foi apagado

    # Criação de novo usuário anônimo
    anon_username = f"anon_{uuid.uuid4().hex[:10]}"
    anon_email = f"{anon_username}@anon.com"

    anon_user = User.objects.create_user(
        username=anon_username,
        email=anon_email,
        password=User.objects.make_random_password(),
        role="anonymous",
    )

    request.session['anon_user_id'] = anon_user.id
    login(request, anon_user)

    return anon_user

@login_required
def criar_conta_real(request):
    user = request.user

    if user.role != 'anonymous':
        messages.info(request, "Sua conta já é uma conta real.")
        return redirect('home')

    if request.method == 'POST':
        form = CriarContaRealForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'default'  # atualiza o tipo de conta
            user.save()
            messages.success(request, "Conta real criada com sucesso!")
            login(request, user)  # garante que ele continua logado
            return redirect('home')
    else:
        form = CriarContaRealForm(instance=user)

    return render(request, 'canionsDoSul_app/criar_conta_real.html', {'form': form})

@login_required
def create_family(request):
    if request.method == 'POST':
        form = FamilyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = FamilyForm()
    return render(request, 'canionsDoSul_app/criar_familia.html', {'form': form})

@login_required
def create_genus(request):
    if request.method == 'POST':
        form = GenusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = GenusForm()
    return render(request, 'canionsDoSul_app/criar_genero.html', {'form': form})

@login_required
def create_species(request):
    if request.method == 'POST':
        form = SpeciesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SpeciesForm()
    return render(request, 'canionsDoSul_app/criar_especie.html', {'form': form})

def create_observation(request):
    return render(request, 'canionsDoSul_app/criar_observacao.html')

def observation_by_latlng(request):
    if request.method == 'POST':
        observation_form = ObservationLatLngForm(request.POST)
        media_form = MediaForm(request.POST, request.FILES)

        city = request.POST.get('city_name')
        state = request.POST.get('state_name')
        country = request.POST.get('country_name', 'Brasil')

        if country.lower() != 'brasil':
            messages.error(request, 'Somente observações no Brasil são permitidas.')
        elif observation_form.is_valid():
            # Criação/Busca de localização
            localization, _ = Localization.objects.get_or_create(
                city_name=city,
                state_name=state,
                country_name=country,
                defaults={'user': request.user if request.user.is_authenticated else None}
            )

            # Pega os dados do form
            family_name = observation_form.cleaned_data['family_name'] or "Desconhecida"
            genus_name = observation_form.cleaned_data['genus_name'] or "Desconhecida"
            species_scientific_name = observation_form.cleaned_data['species_scientific_name'] or "Desconhecida"
            species_popular_name = observation_form.cleaned_data['species_popular_name'] or "Desconhecida"
            notes = observation_form.cleaned_data['notes'] or None
            # habitat = observation_form.cleaned_data['habitat']
            status=observation_form.cleaned_data.get('status', 'Pendente')

            # Criação ou obtenção da família
            family, _ = Family.objects.get_or_create(name=family_name)

            # Criação ou obtenção do gênero vinculado à família
            genus, _ = Genus.objects.get_or_create(name=genus_name, family=family)

            # Criação da espécie vinculada ao gênero
            species, _ = Species.objects.get_or_create(
                popular_name=species_popular_name,
                scientific_name=species_scientific_name,
                genus=genus,
                defaults={
                    # 'habitat': habitat
                    'user': request.user if request.user.is_authenticated else None
                }
            )

            # Criação da observação
            observation = Observation(
                latitude=observation_form.cleaned_data['latitude'],
                longitude=observation_form.cleaned_data['longitude'],
                species=species,
                localization=localization,
                user=get_or_create_anonymous_user(request),
                notes=notes,
                status="Pendente",
            )
            observation.save()

            # Upload de mídia
            if 'files' in request.FILES:
                for file in request.FILES.getlist('files'):
                    media = Media.objects.create(
                        files=file,
                        name=file.name[:255],
                    )
                    ObservationMedia.objects.create(
                        observation=observation,
                        media=media
                    )

            return redirect('home')
        else:
            print(observation_form.errors)

    else:
        observation_form = ObservationLatLngForm()
        media_form = MediaForm()

    return render(request, 'canionsDoSul_app/latlng.html', {
        'observation_form': observation_form,
        'media_form': media_form,
    })

def observation_by_city(request):
    if request.method == 'POST':
        observation_form = ObservationCityForm(request.POST)
        localization_form = LocalizationForm(request.POST)
        media_form = MediaForm(request.POST, request.FILES)

        country = request.POST.get('country_name', '').strip().lower()

        if not country or country != 'brasil':
            messages.error(request, 'Somente observações no Brasil são permitidas.')
            return render(request, 'canionsDoSul_app/cidade.html', {
                'observation_form': observation_form,
                'localization_form': localization_form,
                'media_form': media_form
            })

        if observation_form.is_valid() and localization_form.is_valid():
            localization = localization_form.save(commit=False)
            localization.user = get_or_create_anonymous_user(request)
            localization.save()

            family_name = observation_form.cleaned_data['family_name'] or "Desconhecida"
            genus_name = observation_form.cleaned_data['genus_name'] or "Desconhecida"
            species_scientific_name = observation_form.cleaned_data['species_scientific_name'] or "Desconhecida"
            species_popular_name = observation_form.cleaned_data['species_popular_name'] or "Desconhecida"
            notes = observation_form.cleaned_data['notes'] or None
            status=observation_form.cleaned_data.get('status', 'Pendente')

            # Criação ou obtenção da família
            family, _ = Family.objects.get_or_create(name=family_name)

            # Criação ou obtenção do gênero vinculado à família
            genus, _ = Genus.objects.get_or_create(name=genus_name, family=family)

            # Criação da espécie vinculada ao gênero
            species, _ = Species.objects.get_or_create(
                popular_name=species_popular_name,
                scientific_name=species_scientific_name,
                genus=genus,
                defaults={
                    # 'habitat': habitat,
                    'user': request.user if request.user.is_authenticated else None
                }
            )

            # Criação da observação
            observation = observation_form.save(commit=False)
            observation.localization = localization
            observation.user = get_or_create_anonymous_user(request)
            observation.status = "Pendente"
            observation.species = species
            observation.notes= notes
            observation.save()

            # Upload da mídia
            if 'files' in request.FILES:
                for file in request.FILES.getlist('files'):
                    media = Media.objects.create(
                        files=file,
                        name=file.name[:255]
                    )
                    ObservationMedia.objects.create(
                        observation=observation,
                        media=media
                    )
            return redirect('home')

    else:
        observation_form = ObservationCityForm()
        localization_form = LocalizationForm()
        media_form = MediaForm()

    return render(request, 'canionsDoSul_app/cidade.html', {
        'observation_form': observation_form,
        'localization_form': localization_form,
        'media_form': media_form
    })

@login_required
def observations_list(request):
    search_query = request.GET.get('q', '')
    sort_option = request.GET.get('sort', 'recentes')

    observations = Observation.objects.filter(user=request.user, status='Aprovada').select_related('species', 'localization')

    if search_query:
        observations = observations.filter(species__popular_name__icontains=search_query)

    if sort_option == 'recentes':
        observations = observations.order_by('-created_at')
    elif sort_option == 'antigos':
        observations = observations.order_by('created_at')
    elif sort_option == 'alfabetica':
        observations = observations.order_by('species__popular_name')

    paginator = Paginator(observations, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'canionsDoSul_app/minhas_observacoes.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'sort_option': sort_option,
    })

def all_observations_list(request):
    search_query = request.GET.get('q', '')
    sort_option = request.GET.get('sort', 'recentes')

    observations_list = Observation.objects.filter(status='Aprovada')

    if search_query:
        observations_list = observations_list.filter(
            Q(species__popular_name__icontains=search_query) |
            Q(species__scientific_name__icontains=search_query)
        )

    if sort_option == 'recentes':
        observations_list = observations_list.order_by('-created_at')
    elif sort_option == 'antigos':
        observations_list = observations_list.order_by('created_at')
    elif sort_option == 'alfabetica':
        observations_list = observations_list.order_by('species__popular_name')

    paginator = Paginator(observations_list.select_related('species', 'localization'), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'canionsDoSul_app/observacoes.html', {
        'observations': page_obj,
        'page_obj': page_obj,
        'search_query': search_query,
        'sort_option': sort_option,
    })

def observation_detail(request, pk):
    observation = get_object_or_404(Observation, pk=pk)
    return render(request, 'canionsDoSul_app/detalhes_observacao.html', {'observation': observation})

def my_observation_detail(request, pk):
    observation = get_object_or_404(Observation, pk=pk)
    return render(request, 'canionsDoSul_app/detalhes_minhas_observacoes.html', {'observation': observation})

@login_required
def localization_list_create(request):
    localizations = Localization.objects.filter(user=request.user).order_by('-created_at')
    
    if request.method == 'POST':
        form = LocalizationForm(request.POST)
        if form.is_valid():
            localization = form.save(commit=False)
            localization.user = request.user
            localization.save()
            return redirect('home')
    else:
        form = LocalizationForm()

    return render(request, 'canionsDoSul_app/criar_localizacao.html', {
        'form': form,
        'localizations': localizations
    })

@login_required
@user_passes_test(is_specialist_or_scientist_admin, login_url='erro_permissao')
def lista_observacoes_pendentes(request):
    observacoes = Observation.objects.filter(status='Pendente').order_by('created_at')
    return render(request, 'canionsDoSul_app/lista_observacoes_pendentes.html', {
        'observacoes': observacoes
    })

@login_required
@user_passes_test(is_specialist_or_scientist_admin, login_url='erro_permissao')
def avaliar_observacao_modal(request, observacao_id):
    observacao = get_object_or_404(Observation, id=observacao_id)

    if request.method == 'POST':
        if 'aprovar' in request.POST:
            form = ObservationReviewForm(request.POST, instance=observacao)
            if form.is_valid():
                observacao = form.save(commit=False)
                localization_id = request.POST.get('localization')
                if localization_id:
                    observacao.localization_id = localization_id
                observacao.status = 'Aprovada'
                observacao.species = form.cleaned_data['species']
                observacao.save()

                habitat_input = form.cleaned_data.get('habitat')
                if observacao.species and habitat_input and habitat_input != observacao.species.habitat:
                    observacao.species.habitat = habitat_input
                    observacao.species.save()

                return JsonResponse({'success': True, 'status': 'aprovada'})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
        return JsonResponse({'success': False, 'error': 'Ação inválida'})
    else:
        form = ObservationReviewForm(instance=observacao)
        return render(request, 'canionsDoSul_app/partials/avaliar_observacao_modal.html', {
            'observacao': observacao,
            'form': form
        })

@login_required
@user_passes_test(is_specialist_or_scientist_admin, login_url='erro_permissao')
@csrf_exempt
def rejeitar_observacao(request, observacao_id):
    observacao = get_object_or_404(Observation, id=observacao_id)
    if request.method == 'POST':
        observacao.status = 'Rejeitada'
        observacao.save()
        # observacao.delete()
        return JsonResponse({'success': True, 'status': 'rejeitada'})
    return JsonResponse({'success': False, 'error': 'Rejeição inválida'}, status=400)

@login_required
@user_passes_test(is_admin, login_url='erro_permissao')
def promover_usuario(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        role = request.POST.get("role")  # specialist ou scientist
        user = get_object_or_404(User, id=user_id)

        # Verifica se já não é do tipo
        if role == "specialist" and not hasattr(user, 'specialist'):
            Specialist.objects.create(user=user)
            user.role = "specialist"
            user.save()
        elif role == "scientist" and not hasattr(user, 'scientist'):
            Scientist.objects.create(user=user)
            user.role = "scientist"
            user.save()

        return redirect("promover_usuario")

    usuarios = User.objects.exclude(role="admin")  # Exclui admin da lista
    return render(request, "canionsDoSul_app/promover_usuario.html", {"usuarios": usuarios})

def permission_error(request):
    return render(request, 'canionsDoSul_app/erro_permissao.html')

#Busca acoplada ente familia, genero e espécie
@login_required
def buscar_generos_por_familia(request, family_id):
    generos = Genus.objects.filter(family_id=family_id).values('id', 'name')
    return JsonResponse({'generos': list(generos)})

@login_required
def buscar_especies_por_genero(request, genus_id):
    especies = Species.objects.filter(genus_id=genus_id).values('id', 'scientific_name')
    return JsonResponse({'especies': list(especies)})

@login_required
@user_passes_test(is_specialist_or_scientist_admin, login_url='erro_permissao')
def cadastrar_taxonomia(request):
    if request.method == 'POST':
        family_name = request.POST.get('family', '').strip()
        genus_name = request.POST.get('genus', '').strip()
        species_name = request.POST.get('species', '').strip()
        popular_name = request.POST.get('popular_name', '').strip()
        habitat = request.POST.get('habitat', '').strip()

        # Verifica se já existe a espécie para o gênero informado
        family_obj, _ = Family.objects.get_or_create(name__iexact=family_name, defaults={'name': family_name})
        genus_obj, _ = Genus.objects.get_or_create(name__iexact=genus_name, family=family_obj, defaults={'name': genus_name, 'family': family_obj})
        species_exists = Species.objects.filter(scientific_name__iexact=species_name, genus=genus_obj).exists()

        if species_exists:
            messages.error(request, 'Espécie já cadastrada para esse gênero e familia.')

        else:
            Species.objects.create(
                scientific_name=species_name,
                popular_name=popular_name,
                habitat=habitat,
                genus=genus_obj,
                user=request.user
            )
            messages.success(request, 'Cadeia taxonômica cadastrada com sucesso.')
            return redirect('cadastrar')  # Só redireciona após sucesso

        # Se caiu aqui, houve erro -> renderiza novamente com os valores preenchidos
        context = {
            'familias': Family.objects.all(),
            'generos': Genus.objects.all(),
            'especies': Species.objects.all(),
            'form_values': {
                'family': family_name,
                'genus': genus_name,
                'species': species_name,
                'popular_name': popular_name,
                'habitat': habitat,
            }
        }
        return render(request, 'canionsDoSul_app/cadastrar.html', context)

    # GET
    context = {
        'familias': Family.objects.all(),
        'generos': Genus.objects.all(),
        'especies': Species.objects.all()
    }
    return render(request, 'canionsDoSul_app/cadastrar.html', context)

# @login_required
@csrf_exempt
def autocomplete_family(request):
    term = request.GET.get('term', '')
    families = Family.objects.filter(name__icontains=term).values_list('name', flat=True)
    return JsonResponse(list(families), safe=False)

# @login_required
@csrf_exempt
def autocomplete_genus(request):
    term = request.GET.get('term', '')
    family_name = request.GET.get('family', '')

    if not family_name:
        return JsonResponse([], safe=False)

    try:
        family = Family.objects.get(name__iexact=family_name)
    except Family.DoesNotExist:
        return JsonResponse([], safe=False)

    generos = Genus.objects.filter(
        name__icontains=term,
        family=family
    ).values_list('name', flat=True)

    return JsonResponse(list(generos), safe=False)

# @login_required
@csrf_exempt
def autocomplete_species(request):
    term = request.GET.get('term', '')
    family_name = request.GET.get('family', '')
    genus_name = request.GET.get('genus', '')

    if not family_name or not genus_name:
        return JsonResponse([], safe=False)

    try:
        family = Family.objects.get(name__iexact=family_name)
        genus = Genus.objects.get(name__iexact=genus_name, family=family)
    except (Family.DoesNotExist, Genus.DoesNotExist):
        return JsonResponse([], safe=False)

    especies = Species.objects.filter(
        scientific_name__icontains=term,
        genus=genus
    ).values('scientific_name', 'popular_name')

    return JsonResponse(list(especies), safe=False)

@login_required
def get_specie_habitat(request, especie_id):
    try:
        especie = Species.objects.get(id=especie_id)
        return JsonResponse({'habitat': especie.habitat})
    except Species.DoesNotExist:
        return JsonResponse({'habitat': ''})

@csrf_exempt
def get_habitat(request):
    term = request.GET.get('term', '')
    genus_name = request.GET.get('genus', '')
    family_name = request.GET.get('family', '')

    try:
        family = Family.objects.get(name__iexact=family_name)
        genus = Genus.objects.get(name__iexact=genus_name, family=family)
        species = Species.objects.get(scientific_name__iexact=term, genus=genus)
    except (Family.DoesNotExist, Genus.DoesNotExist, Species.DoesNotExist):
        return JsonResponse({'habitat': ''})

    return JsonResponse({'habitat': species.habitat})

@login_required
@user_passes_test(is_specialist_or_scientist_admin, login_url='erro_permissao')
@require_POST
def excluir_midia_observacao(request, media_id):
    try:
        # Exclui o vínculo
        observation_media = get_object_or_404(ObservationMedia, media_id=media_id)
        media = observation_media.media
        observation_media.delete()

        # Verifica se a mídia não está mais associada a nenhuma observação
        if not ObservationMedia.objects.filter(media=media).exists():
            media.files.delete()  # Remove o arquivo do sistema de arquivos
            media.delete()        # Remove do banco

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

def species_list_view(request):
    query = request.GET.get('q', '')
    species_list = Species.objects.filter(popular_name__icontains=query) if query else Species.objects.all()
    return render(request, 'canionsDoSul_app/listar_especies.html', {'species_list': species_list, 'query': query})


def modal_species_info(request, id):
    species = get_object_or_404(Species, id=id)
    return render(request, 'canionsDoSul_app/partials/info_especies_modal.html', {'species': species})


def modal_edit_species(request, id):
    species = get_object_or_404(Species, id=id)
    if request.method == 'POST':
        species.scientific_name = request.POST['scientific_name']
        species.popular_name = request.POST['popular_name']
        species.habitat = request.POST['habitat']
        species.save()
        return JsonResponse({'success': True})
    return render(request, 'canionsDoSul_app/partials/editar_especies_modal.html', {'species': species})


def modal_delete_species(request, id):
    species = get_object_or_404(Species, id=id)
    if request.method == 'POST':
        species.delete()
        return JsonResponse({'success': True})
    return render(request, 'canionsDoSul_app/partials/deletar_especies_modal.html', {'species': species})