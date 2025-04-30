#imports
from django.shortcuts import render, redirect
from .models import Family, Genus, Species, Observation, Localization
from .forms import FamilyForm, GenusForm, SpeciesForm, ObservationForm, LocalizationForm
from django.contrib.auth.decorators import login_required

#views
def home(request):
    return render(request, 'canionsDoSul_app/home.html')

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

@login_required
def create_observation(request):
    if request.method == 'POST':
        form = ObservationForm(request.POST)
        if form.is_valid():
            observation = form.save(commit=False)
            observation.user = request.user  # Garante segurança e controle
            observation.save()
            return redirect('home')  # Redireciona após cadastro
    else:
        form = ObservationForm()
    return render(request, 'canionsDoSul_app/criar_observacao.html', {'form': form})

@login_required
def observations_list(request):
    observations = Observation.objects.filter(user=request.user).select_related('species', 'localization')
    return render(request, 'canionsDoSul_app/minhas_observacoes.html', {'observations': observations})

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