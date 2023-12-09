from django.contrib import admin
from django.urls import path
from . import views
from .views import index, visualiser,Graphe,Parcoure_donnes

urlpatterns = [
            path('', index, name='index'),
            path('visualiser/',visualiser, name='visualiser'),
            path('Graphe/',Graphe, name='Graphe'),
            path('Parcoure_donnes/',Parcoure_donnes, name='Parcoure_donnes'),
            
]
