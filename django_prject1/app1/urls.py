from django.contrib import admin
from django.urls import path
from . import views
from .views import index, visualiser,Graphe,stats,file_loi_view,test_traitement

urlpatterns = [
            path('', index, name='index'),
            path('visualiser/',visualiser, name='visualiser'),
            path('Graphe/',Graphe, name='Graphe'),
            path('statistiques/',stats, name='statistiques'),
            path('loi/', file_loi_view , name='loi'),
            path('test_traitement',test_traitement,name='test_traitement')
            
]
