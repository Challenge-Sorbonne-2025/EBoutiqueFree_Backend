from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API Free App",
        default_version='v1',
        description="Documentation interactive de l'API pour la gestion de boutiques",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True, #permet l'accés public à la documentation
    permission_classes=[permissions.AllowAny], # Permet à tout le monde d'accéder à Swagger
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('free_app.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
