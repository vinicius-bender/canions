from django import forms
from .models import Family, Genus, Species, Observation, Localization
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, ReadOnlyPasswordHashField

User = get_user_model()

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Confirme a Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        # fields = ['username', 'email', 'role']
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            #'role': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Usuário',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu usuário'
        })
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha'
        })
    )

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