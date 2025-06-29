# canionsDoSul_app/urls.py

from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import CustomLoginView


urlpatterns = [
    path('', views.home, name='home'),
    path("sobre/", views.about, name="sobre"),
    path("contato/", views.contact, name="contato"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registrar/', views.register, name='registrar'),
    path('criar-conta-real/', views.criar_conta_real, name='criar_conta_real'),
    path('painel_administrador/', views.admin_panel, name='admin_panel'),
    path('painel_administrador/cadastrar/', views.cadastrar_taxonomia, name='cadastrar'),
    path('autocomplete-family/', views.autocomplete_family, name='autocomplete_family'),
    path('autocomplete-genus/', views.autocomplete_genus, name='autocomplete_genus'),
    path('autocomplete-species/', views.autocomplete_species, name='autocomplete_species'),
    path('get-habitat/', views.get_habitat, name='get_habitat'),
    path("especies/<int:especie_id>/habitat/", views.get_specie_habitat, name="obter_habitat_especie"),
    path('cadastrar/familia/', views.create_family, name='criar_familia'),
    path('cadastrar/genero/', views.create_genus, name='criar_genero'),
    path('cadastrar/especie/', views.create_species, name='criar_especie'),
    path('criar_observacao/', views.create_observation, name='criar_observacao'),
    path('criar_observacao/latlng/', views.observation_by_latlng, name='latlng'),
    path('criar_observacao/cidade/', views.observation_by_city, name='cidade'),
    path('minhas_observacoes/', views.observations_list, name='minhas_observacoes'),
    path('criar_localizacao/', views.localization_list_create, name='criar_localizacao'),
    path('observacoes/', views.all_observations_list, name='observacoes'),
    path('observacoes/<int:pk>/', views.observation_detail, name='detalhes_observacoes'),
    path('minhas_observacoes/<int:pk>/', views.my_observation_detail, name='detalhes_minhas_observacoes'),
    path('painel_administrador/observacoes_pendentes/', views.lista_observacoes_pendentes, name='lista_observacoes_pendentes'),
    path('observacoes/pendentes/avaliar-observacao/<int:observacao_id>/modal/', views.avaliar_observacao_modal, name='avaliar_observacao_modal'),
    path('observacoes/pendentes/rejeitar-observacao/<int:observacao_id>/', views.rejeitar_observacao, name='rejeitar_observacao'),
    path("painel_administrador/promover_usuario/", views.promover_usuario, name="promover_usuario"),
    path("erro_permissao/", views.permission_error, name="erro_permissao"),
    path('buscar-generos/<int:family_id>/', views.buscar_generos_por_familia, name='buscar_generos'),
    path('buscar-especies/<int:genus_id>/', views.buscar_especies_por_genero, name='buscar_especies'),
    path('observacoes/midia/<int:media_id>/excluir/', views.excluir_midia_observacao, name='excluir_midia_observacao'),
    path('especies/', views.species_list_view, name='listar_especies'),
    path('especie/<int:id>/info/', views.modal_species_info, name='informacoes_especies'),
    path('especie/<int:id>/editar/', views.modal_edit_species, name='editar_especies'),
    path('especie/<int:id>/deletar/', views.modal_delete_species, name='deletar_especies'),
]