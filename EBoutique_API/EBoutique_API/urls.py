"""
URL configuration for EBoutique_API project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from boutique.views import accueil  # afficher la page d’accueil ici

urlpatterns = [
    path("", accueil, name="accueil"),  # Page d'accueil de l'application boutique
    #path("api-auth/", include("rest_framework.urls")),  # API US5 & US6 : recherche de boutiques proches où le stock est non nul
    path("admin/", admin.site.urls),
    path("", include('free_app.urls')),
    path("boutique/", include('boutique.urls')), # URL de l'application boutique
]
