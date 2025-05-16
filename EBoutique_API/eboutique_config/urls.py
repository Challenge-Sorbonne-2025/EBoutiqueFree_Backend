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
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
# from boutique.views import accueil  # afficher la page d’accueil ici


schema_view = get_schema_view(
    openapi.Info(
        title="EBoutique FREE API",
        default_version='v1',
        description="""
API pour la gestion des boutiques de téléphones free les plus proches de vous.

## Authentification
Pour utiliser l'API  afin d'avoir accès aux endpoints lies a la gestion des boutiques, produits, stocks, etc (requete POST, PUT, DELETE) il faut :
1. Obtenez un token JWT via `/api/token/`
2. Cliquez sur le bouton 'Authorize' en haut
3. Collez simplement votre token JWT (avec le préfixe Bearer suivi d'un espace)
""",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@eboutique.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('boutique.urls')),
    path('api/', include('free_app.urls')),
    
    # URLs pour Swagger
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # path("", accueil, name="accueil"),  # Page d'accueil de l'application boutique  |
    # #path("api-auth/", include("rest_framework.urls")),  # API US5 & US6 : recherche de boutiques proches où le stock est non nul

    # path("boutique/", include('boutique.urls')), # URL de l'application boutique
]
