from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recebimentos/', include('recebimentos.urls')),
    path('', lambda r: redirect('recebimentos:dashboard')),
]
