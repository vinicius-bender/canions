#imports
from django.shortcuts import render, redirect
from .models import Family, Genus, Species
from .forms import FamilyForm, GenusForm, SpeciesForm

#views
def home(request):
    return render(request, 'canionsDoSul_app/home.html')

def create_family(request):
    if request.method == 'POST':
        form = FamilyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = FamilyForm()
    return render(request, 'canionsDoSul_app/create_family.html', {'form': form})

def create_genus(request):
    if request.method == 'POST':
        form = GenusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = GenusForm()
    return render(request, 'canionsDoSul_app/create_genus.html', {'form': form})

def create_species(request):
    if request.method == 'POST':
        form = SpeciesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SpeciesForm()
    return render(request, 'canionsDoSul_app/create_species.html', {'form': form})