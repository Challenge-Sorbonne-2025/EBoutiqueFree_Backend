from django.urls import path
from .views import recherche_produits_par_adresse
urlpatterns = [
    path('api/recherche-produits/', recherche_produits_par_adresse, name='recherche_par_adresse'),
]
