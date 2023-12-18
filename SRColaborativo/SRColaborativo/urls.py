"""
URL configuration for SRColaborativo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from principal import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio),
    path('populate/', views.populate),
    path('ingresar/', views.ingresar),
    path('loadRS/', views.loadRS),
    path('recomendar_peliculas_usuarios/', views.recomendar_peliculas_usuarios),
    path('recomendar_peliculas_usuarios_items/', views.recomendar_peliculas_usuarios_items),
    path('peliculas_similares/', views.peliculas_similares),
    path('usuarios_recomendados/', views.usuarios_recomendados),
    path('puntuaciones_usuario/', views.puntuaciones_usuario),
]
