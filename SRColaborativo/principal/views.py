from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from principal.forms import *
from principal.utils import getPuntuacionesUsuario

from principal.populate import populateDB, populateRS

# Create your views here.
def inicio(request):
    return render(request, 'base.html')

@login_required(login_url = '/ingresar')
def populate(request):
    (o,g,u,m,p)=populateDB()
    mensaje = 'Se han cargado: ' + str(o) + ' ocupaciones ;' + str(g) + ' generos ;' + str(u) + ' usuarios ;' + str(m) + ' peliculas ;' + str(p) + ' puntuaciones'
    logout(request)  # se hace logout para obligar a login cada vez que se vaya a poblar la BD
    return render(request, 'cargar.html',{'titulo':'FIN DE CARGA DE LA BD','mensaje':mensaje,'STATIC_URL':settings.STATIC_URL})

def ingresar(request):
    formulario = AuthenticationForm()
    if request.method=='POST':
        formulario = AuthenticationForm(request.POST)
        usuario=request.POST['username']
        clave=request.POST['password']
        acceso=authenticate(username=usuario,password=clave)
        if acceso is not None:
            if acceso.is_active:
                login(request, acceso)
                return (HttpResponseRedirect('/populate'))
            else:
                return render(request, 'mensaje_error.html',{'error':"USUARIO NO ACTIVO",'STATIC_URL':settings.STATIC_URL})
        else:
            return render(request, 'mensaje_error.html',{'error':"USUARIO O CONTRASEÑA INCORRECTOS",'STATIC_URL':settings.STATIC_URL})
    
    return render(request, 'ingresar.html', {'formulario':formulario, 'STATIC_URL':settings.STATIC_URL})

def loadRS(request):
    RS = populateRS()
    mensaje = 'Se ha cargado el Sistema de Recomendacion!'
    return render(request, 'cargar.html', {'titulo':'FIN DE CARGA DE RS','mensaje':mensaje,'STATIC_URL':settings.STATIC_URL})

def recomendar_peliculas_usuarios(request):
    return render(request, 'recomendar_peliculas_usuarios.html', {'STATIC_URL':settings.STATIC_URL})

def recomendar_peliculas_usuarios_items(request):
    return render(request, 'recomendar_peliculas_usuarios_items.html', {'STATIC_URL':settings.STATIC_URL})

def peliculas_similares(request):
    return render(request, 'peliculas_similares.html', {'STATIC_URL':settings.STATIC_URL})

def usuarios_recomendados(request):
    return render(request, 'usuarios_recomendados.html', {'STATIC_URL':settings.STATIC_URL})

def puntuaciones_usuario(request):
    if request.method=='POST':
        formulario = puntuaciones_usuario(request.POST)
        if formulario.is_valid():
            id_usuario = formulario.cleaned_data['id_usuario']
            puntuaciones = getPuntuacionesUsuario(id_usuario)
            mensaje = ''
            for puntuacion in puntuaciones:
                mensaje += f'Pelicula {puntuacion} puntuacion {puntuaciones[puntuacion]}\n'
            return render(request, 'cargar.html', {'titulo':f'Puntuaciones de {id_usuario}:', 'mensaje':f'{mensaje}', 'STATIC_URL':settings.STATIC_URL})
    else:
        formulario = puntuaciones_usuario_form()
    return render(request, 'puntuaciones_usuario.html', {'titulo':'Buscar puntuaciones por usuario', 'mensaje':'Introduzca un ID de usuario:','form':formulario,'STATIC_URL':settings.STATIC_URL})