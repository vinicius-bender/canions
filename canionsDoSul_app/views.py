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

#views
def is_specialist_or_scientist(user):
    return user.role in ['specialist', 'scientist']

def is_specialist_or_scientist_admin(user):
    return user.role in ['specialist', 'scientist', 'admin']

def is_admin(user):
    return user.is_authenticated and user.role == "admin"

def home(request):
    return render(request, 'canionsDoSul_app/home.html', {'user': request.user})

@login_required
def cadastrar(request):
    return render(request, 'canionsDoSul_app/cadastrar.html')

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
    
    # return render(request, 'canionsDoSul_app/minhas_observacoes.html', {'observations': observations})

# def all_observations_list(request):
#     observations_list = Observation.objects.all().select_related('species', 'localization').order_by('-created_at')
#     paginator = Paginator(observations_list, 10)

#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     return render(request, 'canionsDoSul_app/observacoes.html', {
#         'observations': page_obj,
#         'page_obj': page_obj
#     })

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

# @login_required
# def edit_observation(request, observation_id):
#     observation = get_object_or_404(Observation, id=observation_id, user=request.user)
#     if request.method == 'POST':
#         form = ObservationForm(request.POST, instance=observation)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Observação atualizada com sucesso!")
#             return redirect('minhas_observacoes')
#     else:
#         form = ObservationForm(instance=observation)
#     return render(request, 'canionsDoSul_app/editar_observacoes.html', {'form': form})

# @login_required
# def delete_observation(request, observation_id):
#     observation = get_object_or_404(Observation, id=observation_id, user=request.user)
#     if request.method == 'POST':
#         observation.delete()
#         messages.success(request, "Observação excluída com sucesso!")
#         return redirect('minhas_observacoes')
#     return render(request, 'canionsDoSul_app/deletar_observacoes.html', {'observation': observation})

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
    observacoes = Observation.objects.filter(species__isnull=True)
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