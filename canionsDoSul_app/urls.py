# canionsDoSul_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastrar/familia/', views.create_family, name='create_family'),
    path('cadastrar/genero/', views.create_genus, name='create_genus'),
    path('cadastrar/especie/', views.create_species, name='create_species'),
]