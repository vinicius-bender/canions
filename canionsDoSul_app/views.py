#imports
from django.shortcuts import render, redirect, get_object_or_404
from .models import Family, Genus, Species, Observation, Localization, Media, ObservationMedia
from .forms import FamilyForm, GenusForm, SpeciesForm, ObservationForm, LocalizationForm, CustomLoginForm, CustomUserCreationForm, ObservationForm, MediaForm, MultipleFileInput
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.core.paginator import Paginator

#views
def home(request):
    return render(request, 'canionsDoSul_app/home.html')

@login_required
def cadastrar(request):
    return render(request, 'canionsDoSul_app/cadastrar.html')

class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = 'canionsDoSul_app/login.html'

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redireciona após cadastro
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

# @login_required
# def create_observation(request):
#     if request.method == 'POST':
#         form = ObservationForm(request.POST)
#         if form.is_valid():
#             observation = form.save(commit=False)
#             observation.user = request.user  # Garante segurança e controle
#             observation.save()
#             return redirect('home')  # Redireciona após cadastro
#     else:
#         form = ObservationForm()
#     return render(request, 'canionsDoSul_app/criar_observacao.html', {'form': form})

def create_observation(request):
    if request.method == 'POST':
        observation_form = ObservationForm(request.POST)
        media_form = MediaForm(request.POST, request.FILES)
        
        if observation_form.is_valid():
            # Salva a observação, mas não comita ainda
            observation = observation_form.save(commit=False)
            observation.user = request.user
            observation.save()
            
            # Processa as imagens
            if 'images' in request.FILES:
                for image in request.FILES.getlist('images'):
                    # Cria um objeto Media para cada imagem
                    media = Media(
                        name=f"Imagem de {observation.species.popular_name}",
                        image=image
                    )
                    media.save()
                    
                    # Cria a relação entre observação e mídia
                    observation_media = ObservationMedia(
                        observation=observation,
                        media=media
                    )
                    observation_media.save()
            
            return redirect('minhas_observacoes')
    else:
        observation_form = ObservationForm()
        media_form = MediaForm()
    
    return render(request, 'canionsDoSul_app/criar_observacao.html', {
        'observation_form': observation_form,
        'media_form': media_form
    })

@login_required
def observations_list(request):
    observations = Observation.objects.filter(user=request.user).select_related('species', 'localization')
    paginator = Paginator(observations, 10)  # 10 observações por página

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'canionsDoSul_app/minhas_observacoes.html', {
        'observations': page_obj,  # ainda pode usar o mesmo nome no template
        'page_obj': page_obj       # útil para navegação
    })
    
    # return render(request, 'canionsDoSul_app/minhas_observacoes.html', {'observations': observations})

def all_observations_list(request):
    observations_list = Observation.objects.all().select_related('species', 'localization')
    paginator = Paginator(observations_list, 10)  # 10 observações por página

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'canionsDoSul_app/observacoes.html', {
        'observations': page_obj,  # ainda pode usar o mesmo nome no template
        'page_obj': page_obj       # útil para navegação
    })

@login_required
def edit_observation(request, observation_id):
    observation = get_object_or_404(Observation, id=observation_id, user=request.user)
    if request.method == 'POST':
        form = ObservationForm(request.POST, instance=observation)
        if form.is_valid():
            form.save()
            messages.success(request, "Observação atualizada com sucesso!")
            return redirect('minhas_observacoes')
    else:
        form = ObservationForm(instance=observation)
    return render(request, 'canionsDoSul_app/editar_observacoes.html', {'form': form})

@login_required
def delete_observation(request, observation_id):
    observation = get_object_or_404(Observation, id=observation_id, user=request.user)
    if request.method == 'POST':
        observation.delete()
        messages.success(request, "Observação excluída com sucesso!")
        return redirect('minhas_observacoes')
    return render(request, 'canionsDoSul_app/deletar_observacoes.html', {'observation': observation})

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