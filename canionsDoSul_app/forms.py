from django import forms
# from django.forms.widgets import ClearableFileInput
from django.forms.widgets import Widget, Input
from django.utils.html import format_html
from .models import Family, Genus, Species, Observation, Localization, Media, ObservationMedia
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, ReadOnlyPasswordHashField

User = get_user_model()

# Widget personalizado para upload de múltiplos arquivos
class MultipleFileInput(Input):
    input_type = 'file'
    needs_multipart_form = True
    
    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs['multiple'] = True
        self.attrs['accept'] = 'image/*,video/*'  #abre a galeria no celular
    
    def value_from_datadict(self, data, files, name):
        if hasattr(files, 'getlist'):
            return files.getlist(name)
        return files.get(name)

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite sua senha',
        }),
    )
    password2 = forms.CharField(
        label='Confirme a Senha',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite novamente sua senha',
        }),
    )

    class Meta:
        model = User
        # fields = ['username', 'email', 'role']
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
            'placeholder': 'Digite o seu nome de usuário',
        }),
            'email': forms.EmailInput(attrs={
            'placeholder': 'Exemplo@gmail.com',
        }),
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
        user.role = "default"  # Atribuição automática da role
        if commit:
            user.save()
        return user

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Digite seu e-mail',
        widget=forms.TextInput(attrs={
            'placeholder': 'Exemplo@gmail.com',
        }),
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite sua senha',
        }),
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

class LocalizationForm(forms.ModelForm):
    class Meta:
        model = Localization
        fields = ['city_name', 'state_name', 'country_name']
        widgets = {
            'city_name': forms.TextInput(attrs={'class': 'form-control',
            'id': 'id_city_name',
            }),
            'state_name': forms.TextInput(attrs={'class': 'form-control',
            'id': 'id_state_name',
            }),
            'country_name': forms.HiddenInput(attrs={'class': 'form-control', 
            'id': 'id_country_name',
            }),
            # 'country_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

# class ObservationLatLngForm(forms.ModelForm):
#     class Meta:
#         model = Observation
#         # fields = ['latitude', 'longitude', 'species']
#         fields = ['latitude', 'longitude']
#         widgets = {
#             'latitude': forms.NumberInput(attrs={
#                 'step': '0.00000001',
#                 'placeholder': 'Ex: -29.12345678',
#                 'id': 'id_latitude',
#             }),
#             'longitude': forms.NumberInput(attrs={
#                 'step': '0.00000001',
#                 'placeholder': 'Ex: -51.23456789',
#                 'id': 'id_longitude'
#             }),
#         }
class ObservationLatLngForm(forms.ModelForm):
    family_name = forms.CharField(max_length=255, required=False, label="Família")
    genus_name = forms.CharField(max_length=255, required=False, label="Gênero")
    species_scientific_name = forms.CharField(max_length=255, required=False, label="Espécie (nome popular)")
    species_popular_name = forms.CharField(max_length=255, required=False, label="Nome Científico")
    notes = forms.CharField(widget=forms.Textarea, required=False, label="Observações adicionais")

    class Meta:
        model = Observation
        fields = ['latitude', 'longitude']
        widgets = {
            'latitude': forms.NumberInput(attrs={
                'step': '0.00000001',
                'placeholder': 'Ex: -29.12345678',
                'id': 'id_latitude',
            }),
            'longitude': forms.NumberInput(attrs={
                'step': '0.00000001',
                'placeholder': 'Ex: -51.23456789',
                'id': 'id_longitude'
            }),
        }

# class ObservationCityForm(forms.ModelForm):
#     class Meta:
#         model = Observation
#         exclude = ['species', 'status', 'user', 'medias']
#         widgets = {
#             'latitude': forms.HiddenInput(attrs={
#                 'id': 'id_latitude',
#             }),
#             'longitude': forms.HiddenInput(attrs={
#                 'id': 'id_longitude',
#             }),
#         }
class ObservationCityForm(forms.ModelForm):
    family_name = forms.CharField(max_length=255, required=False, label="Família")
    genus_name = forms.CharField(max_length=255, required=False, label="Gênero")
    species_scientific_name = forms.CharField(max_length=255, required=False, label="Nome Científico")
    species_popular_name = forms.CharField(max_length=255, required=False, label="Espécie (nome popular)")
    notes = forms.CharField(widget=forms.Textarea, required=False, label="Observações adicionais")

    class Meta:
        model = Observation
        exclude = ['species', 'status', 'user', 'medias']
        widgets = {
            'latitude': forms.HiddenInput(attrs={'id': 'id_latitude'}),
            'longitude': forms.HiddenInput(attrs={'id': 'id_longitude'}),
        }
ObservationCityForm.localization = LocalizationForm()

# class ObservationReviewForm(forms.ModelForm):
#     family = forms.ModelChoiceField(queryset=Family.objects.all(), required=False, label="Família")
#     genus = forms.ModelChoiceField(queryset=Genus.objects.none(), required=False, label="Gênero")
#     species = forms.ModelChoiceField(queryset=Species.objects.none(), required=False, label="Espécie")

#     class Meta:
#         model = Observation
#         fields = ['family', 'genus', 'species', 'latitude', 'longitude']
#         widgets = {
#             'latitude': forms.NumberInput(attrs={
#                 'step': '0.00000001',
#                 'placeholder': 'Ex: -29.12345678',
#             }),
#             'longitude': forms.NumberInput(attrs={
#                 'step': '0.00000001',
#                 'placeholder': 'Ex: -51.23456789',
#             }),
#         }
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         # Caso esteja editando uma instância já salva
#         if self.instance and self.instance.species:
#             genus = self.instance.species.genus
#             family = genus.family if genus else None

#             if family:
#                 self.fields['genus'].queryset = Genus.objects.filter(family=family)
#             if genus:
#                 self.fields['species'].queryset = Species.objects.filter(genus=genus)

#         # Se os dados foram enviados no POST
#         if 'family' in self.data:
#             try:
#                 family_id = int(self.data.get('family'))
#                 self.fields['genus'].queryset = Genus.objects.filter(family_id=family_id)
#             except (ValueError, TypeError):
#                 pass

#         if 'genus' in self.data:
#             try:
#                 genus_id = int(self.data.get('genus'))
#                 self.fields['species'].queryset = Species.objects.filter(genus_id=genus_id)
#             except (ValueError, TypeError):
#                 pass

#     def clean_species(self):
#         species = self.cleaned_data.get('species')
#         if not species:
#             raise forms.ValidationError("É necessário selecionar uma espécie.")
#         return species
class ObservationReviewForm(forms.ModelForm):
    # family = forms.ModelChoiceField(queryset=Family.objects.all(), required=False, label="Família")
    # genus = forms.ModelChoiceField(queryset=Genus.objects.none(), required=False, label="Gênero")
    # species = forms.ModelChoiceField(queryset=Species.objects.none(), required=False, label="Espécie")
    # notes = forms.CharField(widget=forms.Textarea, required=False, label="Observações adicionais")
    # habitat = forms.CharField(widget=forms.Textarea, required=False, label="Informações sobre a espécie")

    family = forms.CharField(required=False, label="Família")
    genus = forms.CharField(required=False, label="Gênero")
    species = forms.CharField(required=False, label="Espécie")
    notes = forms.CharField(widget=forms.Textarea, required=False, label="Observações adicionais")
    habitat = forms.CharField(widget=forms.Textarea, required=False, label="Informações sobre a espécie")

    class Meta:
        model = Observation
        fields = ['family', 'genus', 'species', 'latitude', 'longitude', 'notes']
        widgets = {
            'latitude': forms.NumberInput(attrs={
                'step': '0.00000001',
                'placeholder': 'Ex: -29.12345678',
            }),
            'longitude': forms.NumberInput(attrs={
                'step': '0.00000001',
                'placeholder': 'Ex: -51.23456789',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.species:
            species = self.instance.species
            genus = species.genus
            family = genus.family
            self.fields['family'].initial = family.name
            self.fields['genus'].initial = genus.name
            self.fields['species'].initial = species.scientific_name
            self.fields['habitat'].initial = species.habitat
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

        # self.fields['genus'].queryset = Genus.objects.none()
        # self.fields['species'].queryset = Species.objects.none()

        # if self.instance and self.instance.species:
        #     species = self.instance.species
        #     genus = species.genus
        #     family = genus.family if genus else None
        #     self.fields['habitat'].initial = self.instance.species.habitat
        #     # self.fields['habitat'].widget.attrs['readonly'] = True

        #     # Preenche os campos visuais
        #     if family:
        #         self.fields['family'].initial = family.pk
        #         self.fields['genus'].queryset = Genus.objects.filter(family=family)

        #     if genus:
        #         self.fields['genus'].initial = genus.pk
        #         self.fields['species'].queryset = Species.objects.filter(genus=genus)

        #     self.fields['species'].initial = species.pk    

        # # Atualização dinâmica no POST
        # if 'family' in self.data:
        #     try:
        #         family_id = int(self.data.get('family'))
        #         self.fields['genus'].queryset = Genus.objects.filter(family_id=family_id)
        #     except (ValueError, TypeError):
        #         pass

        # if 'genus' in self.data:
        #     try:
        #         genus_id = int(self.data.get('genus'))
        #         self.fields['species'].queryset = Species.objects.filter(genus_id=genus_id)
        #     except (ValueError, TypeError):
        #         pass

    # def clean_species(self):
    #     species = self.cleaned_data.get('species')
    #     if not species:
    #         raise forms.ValidationError("É necessário selecionar uma espécie.")
    #     return species

    def clean_species(self):
        family_name = self.cleaned_data.get('family', '').strip()
        genus_name = self.cleaned_data.get('genus', '').strip()
        species_name = self.cleaned_data.get('species', '').strip()

        try:
            family = Family.objects.get(name__iexact=family_name)
            genus = Genus.objects.get(name__iexact=genus_name, family=family)
            species = Species.objects.get(scientific_name__iexact=species_name, genus=genus)
        except (Family.DoesNotExist, Genus.DoesNotExist, Species.DoesNotExist):
            raise forms.ValidationError("Espécie inválida ou não encontrada.")

        return species

# Formulário para upload de múltiplas imagens
class MediaForm(forms.Form):
    files = forms.FileField(
        widget=MultipleFileInput(),
        # label='Selecione arquivos de imagem ou vídeo',
        required=True,
    )

class AprovarObservacaoForm(forms.ModelForm):
    class Meta:
        model = Observation
        fields = ['species']  # ou outros campos editáveis

class CriarContaRealForm(forms.ModelForm):
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Confirme a Senha', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password != password_confirm:
            self.add_error('password_confirm', "As senhas não coincidem.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user