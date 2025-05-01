from django.urls import path
from apps.boutique import views
from .views import tableau_bord

app_name = 'boutique'
urlpatterns = [
    path('tableau-bord/', views.tableau_bord, name='tableau_bord'),
      
]
