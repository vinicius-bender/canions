from django import forms
from .models import Family, Genus, Species, Observation, Localization

class FamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = ['name']

class GenusForm(forms.ModelForm):
    class Meta:
        model = Genus
        fields = ['name', 'family']

class SpeciesForm(forms.ModelForm):
    class Meta:
        model = Species
        fields = ['scientific_name', 'popular_name', 'habitat', 'genus', 'user']

class ObservationForm(forms.ModelForm):
    class Meta:
        model = Observation
        fields = ['longitude', 'latitude', 'species', 'localization']

class LocalizationForm(forms.ModelForm):
    class Meta:
        model = Localization
        fields = ['city_name', 'state_name']
        widgets = {
            'city_name': forms.TextInput(attrs={'class': 'form-control'}),
            'state_name': forms.TextInput(attrs={'class': 'form-control'}),
        }