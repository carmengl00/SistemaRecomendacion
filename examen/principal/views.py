import shelve
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from principal.populate import populateDB

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

def loadDict():
    pass

def loadRS(request):
    loadDict()
    mensaje = 'Se ha cargado el RS'
    return render(request, 'cargar.html', {'titulo': 'FIN DE CARGA DEL RS', 'mensaje': mensaje, 'STATIC_URL': settings.STATIC_URL})

