# canionsDoSul_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastrar/familia/', views.create_family, name='criar_familia'),
    path('cadastrar/genero/', views.create_genus, name='criar_genero'),
    path('cadastrar/especie/', views.create_species, name='criar_especie'),
    path('cadastrar/criar_observacao/', views.create_observation, name='criar_observacao'),
    path('minhas_observacoes/editar/<int:observation_id>/', views.edit_observation, name='edit_observation'),
    path('minhas_observacoes/deletar/<int:observation_id>/', views.delete_observation, name='delete_observation'),
    path('minhas_observacoes/', views.observations_list, name='minhas_observacoes'),
    path('criar_localizacao/', views.localization_list_create, name='criar_localizacao'),
]