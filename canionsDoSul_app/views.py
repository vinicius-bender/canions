#imports
from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Specialist, Scientist, Family, Genus, Species, Observation, Localization, Media, ObservationMedia
from .forms import FamilyForm, GenusForm, SpeciesForm, LocalizationForm, CustomLoginForm, CustomUserCreationForm, MediaForm, MultipleFileInput, ObservationLatLngForm, ObservationCityForm, AprovarObservacaoForm, ObservationReviewForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

#views
def is_specialist_or_scientist(user):
    return user.role in ['specialist', 'scientist']

def is_specialist_or_scientist_admin(user):
    return user.role in ['specialist', 'scientist', 'admin']

def is_admin(user):
    return user.is_authenticated and user.role == "admin"

def home(request):

    # Número de espécies com pelo menos uma observação associada
    num_species = Species.objects.filter(observation__isnull=False).distinct().count()

    # Total de registros (todas as observações, independente do status)
    num_records = Observation.objects.count()

    # Total de observações aprovadas
    num_approved_observations = Observation.objects.filter(status='Aprovada').count()

    context = {
        'user': request.user,
        'num_species': num_species,
        'num_records': num_records,
        'num_approved_observations': num_approved_observations,
    }

    return render(request, 'canionsDoSul_app/home.html', context)

def about(request):
    return render(request, 'canionsDoSul_app/sobre.html')

def contact(request):
    return render(request, 'canionsDoSul_app/contato.html')

@login_required
@user_passes_test(is_admin, login_url='erro_permissao')
def admin_panel(request):
    return render(request, 'canionsDoSul_app/painel_administrador.html')

# @login_required
# def cadastrar(request):
#     return render(request, 'canionsDoSul_app/cadastrar.html')

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

        # Pega os dados de localização preenchidos via JS
        city = request.POST.get('city_name')
        state = request.POST.get('state_name')
        country = request.POST.get('country_name', 'Brasil')  # Default para Brasil

        if observation_form.is_valid():
            # Cria ou obtém a localização
            localization, created = Localization.objects.get_or_create(
                city_name=city,
                state_name=state,
                country_name=country,
                defaults={'user': request.user if request.user.is_authenticated else None}
            )

            observation = observation_form.save(commit=False)
            observation.localization = localization
            observation.user = request.user
            observation.status = observation_form.cleaned_data.get('status', 'Pendente')  # Status default
            observation.save()

            # Processa as imagens
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
        'media_form': media_form
    })

def observation_by_city(request):
    if request.method == 'POST':
        observation_form = ObservationCityForm(request.POST)
        localization_form = LocalizationForm(request.POST)
        media_form = MediaForm(request.POST, request.FILES)

        if observation_form.is_valid() and localization_form.is_valid():
            localization = localization_form.save(commit=False)
            localization.user = request.user
            localization.save()

            observation = observation_form.save(commit=False)
            observation.localization = localization
            observation.user = request.user
            observation.status = "Pendente"
            observation.save()

            # for file in request.FILES.getlist('images'):
            #     Media.objects.create(observation=observation, file=file)
            
            # Processa as imagens
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
    observations = Observation.objects.filter(user=request.user, status='Aprovada') \
        .select_related('species', 'localization') \
        .order_by('-created_at')
    
    paginator = Paginator(observations, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'canionsDoSul_app/minhas_observacoes.html', {
        'observations': page_obj,
        'page_obj': page_obj
    })

def all_observations_list(request):
    observations_list = Observation.objects.filter(status='Aprovada') \
        .select_related('species', 'localization') \
        .order_by('-created_at')

    paginator = Paginator(observations_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'canionsDoSul_app/observacoes.html', {
        'observations': page_obj,
        'page_obj': page_obj
    })

def observation_detail(request, pk):
    observation = get_object_or_404(Observation, pk=pk)
    return render(request, 'canionsDoSul_app/detalhes_observacao.html', {'observation': observation})

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
    observacoes = Observation.objects.filter(species__isnull=True).order_by('created_at')
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
                observacao.save()
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
        observacao.delete()
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

        # 1. Verificar e/ou criar Família
        family_obj, _ = Family.objects.get_or_create(name__iexact=family_name, defaults={'name': family_name})

        # 2. Verificar se já existe um gênero com esse nome para essa família
        genus_obj, _ = Genus.objects.get_or_create(name__iexact=genus_name, family=family_obj, defaults={'name': genus_name, 'family': family_obj})

        # 3. Verificar se a espécie já está cadastrada com esse nome científico e gênero
        species_exists = Species.objects.filter(
            scientific_name__iexact=species_name,
            genus=genus_obj
        ).exists()

        if species_exists:
            messages.warning(request, 'Espécie já cadastrada para esse gênero.')
        else:
            Species.objects.create(
                scientific_name=species_name,
                popular_name=popular_name,
                habitat=habitat,
                genus=genus_obj,
                user=request.user
            )
            messages.success(request, 'Cadeia taxonômica cadastrada com sucesso.')

        return redirect('cadastrar')

    context = {
        'familias': Family.objects.all(),
        'generos': Genus.objects.all(),
        'especies': Species.objects.all()
    }
    return render(request, 'canionsDoSul_app/cadastrar.html', context)

@login_required
@csrf_exempt
def autocomplete_family(request):
    term = request.GET.get('term', '')
    families = Family.objects.filter(name__icontains=term).values_list('name', flat=True)
    return JsonResponse(list(families), safe=False)

@login_required
@csrf_exempt
def autocomplete_genus(request):
    term = request.GET.get('term', '')
    genera = Genus.objects.filter(name__icontains=term).values_list('name', flat=True)
    return JsonResponse(list(genera), safe=False)

@login_required
@csrf_exempt
def autocomplete_species(request):
    term = request.GET.get('term', '')
    especies = Species.objects.filter(scientific_name__icontains=term).values('scientific_name', 'popular_name')
    return JsonResponse(list(especies), safe=False)