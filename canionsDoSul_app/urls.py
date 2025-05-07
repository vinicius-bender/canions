# canionsDoSul_app/urls.py

from django.urls import path
from . import views
from .views import CustomLoginView

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('registrar/', views.register, name='registrar'),
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('cadastrar/familia/', views.create_family, name='criar_familia'),
    path('cadastrar/genero/', views.create_genus, name='criar_genero'),
    path('cadastrar/especie/', views.create_species, name='criar_especie'),
    path('cadastrar/criar_observacao/', views.create_observation, name='criar_observacao'),
    path('minhas_observacoes/editar/<int:observation_id>/', views.edit_observation, name='editar_observacoes'),
    path('minhas_observacoes/deletar/<int:observation_id>/', views.delete_observation, name='deletar_observacoes'),
    path('minhas_observacoes/', views.observations_list, name='minhas_observacoes'),
    path('criar_localizacao/', views.localization_list_create, name='criar_localizacao'),
]