from django.urls import path
from . import views

app_name = "recebimentos"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("listar/", views.listar, name="listar"),
    path("novo/", views.criar, name="criar"),
    path("<int:pk>/", views.detalhe, name="detalhe"),
    path("<int:pk>/editar/", views.editar, name="editar"),
    path("<int:pk>/excluir/", views.excluir, name="excluir"),
]
