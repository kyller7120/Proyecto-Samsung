from django.urls import path
from . import views
urlpatterns = [
    #vista inicial
    path('', views.index),
    path('/equipo_search/', views.search_team, name = 'search_team'),
    path('/plantilla/<str:nombre_equipo>/<int:id_equipo>', views.plantilla_team, name = 'plantilla_team'),
    path('/jugadores/<str:nombre_equipo>/<int:id_equipo>', views.jugadores, name = 'jugadores_team'),
]