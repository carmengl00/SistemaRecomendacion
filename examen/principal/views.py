#encoding latin-1
import shelve
from principal.models import *
from principal.recommendations import *
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from principal.populate import populateDB

def inicio(request):
    return render(request, 'base.html')

def populate(request):
    (peli,punt)=populateDB()
    mensaje = 'Se han cargado: ' + str(peli) + ' películas y ' + str(punt) + ' puntuaciones.'
    return render(request, 'cargar.html',{'titulo':'FIN DE CARGA DE LA BD','mensaje':mensaje,'STATIC_URL':settings.STATIC_URL})

def loadDict():
    Prefs = {}
    shelf = shelve.open("dataRS.dat")
    ratings = Puntuacion.objects.all()
    for r in ratings:
        user = r.usuario.idUsuario
        item = r.pelicula.idPelicula
        rating = r.puntuacion
        Prefs.setdefault(user, {})
        Prefs[user][item] = float(rating)
    shelf['Prefs'] = Prefs
    shelf['ItemsPrefs'] = transformPrefs(Prefs)
    shelf['SimItems']=calculateSimilarItems(Prefs, n=10)
    shelf.close()
    pass

def loadRS(request):
    loadDict()
    mensaje = 'Se ha cargado el RS.'
    return render(request, 'cargar.html', {'titulo': 'FIN DE CARGA DEL RS', 'mensaje': mensaje, 'STATIC_URL': settings.STATIC_URL})

def peliculas_por_actor(request):
    pass

def usuarios_mas_activos(request):
    pass