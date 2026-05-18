from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('gasto/novo/', views.cadastrar_gasto, name='cadastrar_gasto'),
    path('recebimento/novo/', views.cadastrar_recebimento, name='cadastrar_recebimento'),
    path('logs/', views.listar_logs, name='listar_logs'),
]
