# canionsDoSul_app/urls.py

from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import CustomLoginView


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registrar/', views.register, name='registrar'),
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('cadastrar/familia/', views.create_family, name='criar_familia'),
    path('cadastrar/genero/', views.create_genus, name='criar_genero'),
    path('cadastrar/especie/', views.create_species, name='criar_especie'),
    path('criar_observacao/', views.create_observation, name='criar_observacao'),
    path('criar_observacao/latlng/', views.observation_by_latlng, name='latlng'),
    path('criar_observacao/cidade/', views.observation_by_city, name='cidade'),
    path('minhas_observacoes/editar/<int:observation_id>/', views.edit_observation, name='editar_observacoes'),
    path('minhas_observacoes/deletar/<int:observation_id>/', views.delete_observation, name='deletar_observacoes'),
    path('minhas_observacoes/', views.observations_list, name='minhas_observacoes'),
    path('criar_localizacao/', views.localization_list_create, name='criar_localizacao'),
    path('observacoes/', views.all_observations_list, name='observacoes'),
    path('observacoes/pendentes/', views.lista_observacoes_pendentes, name='lista_observacoes_pendentes'),
    path('observacoes/avaliar/<int:observacao_id>/', views.aprovar_observacao, name='aprovar_observacao_detalhes'),
    path("promover_usuario/", views.promover_usuario, name="promover_usuario"),
    path("erro_permissao/", views.permission_error, name="erro_permissao"),
]