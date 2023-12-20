import shelve
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Pelicula, Puntuacion, Usuario
from .recommendations import calculateSimilarItems, getRecommendations, getRecommendedItems, topMatches, transformPrefs
from .forms import BusquedaPeliculaForm, BusquedaUsuarioIdForm

from principal.populate import populateDB

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

def loadRS(request):
    loadDict()
    mensaje = 'Se ha cargado el RS'
    return render(request, 'cargar.html', {'titulo': 'FIN DE CARGA DEL RS', 'mensaje': mensaje, 'STATIC_URL': settings.STATIC_URL})

def recomendar_peliculas_usuarios(request):
    form = BusquedaUsuarioIdForm()
    items = None
    usuario = None

    if request.method == 'POST':
        form = BusquedaUsuarioIdForm(request.POST)

        if form.is_valid():
            idUsuario=form.cleaned_data['idUsuario']
            usuario = get_object_or_404(Usuario, pk=idUsuario)
            shelf = shelve.open("dataRS.dat")
            Prefs = shelf['Prefs']
            shelf.close()

            rankings = getRecommendations(Prefs, int(idUsuario))
            recomendadas = rankings[:2]
            peliculas = []
            puntuaciones = []
            for re in recomendadas:
                peliculas.append(Pelicula.objects.get(pk=re[1]))
                puntuaciones.append(re[0])
            items = zip(peliculas, puntuaciones)
    
    return render(request, 'dos_pelis.html', {'form': form, 'items': items, 'usuario': usuario, 'STATIC_URL': settings.STATIC_URL})

def recomendar_peliculas_usuarios_items(request):
    form = BusquedaUsuarioIdForm()
    items = None
    usuario = None

    if request.method == 'POST':
        form = BusquedaUsuarioIdForm(request.POST)

        if form.is_valid():
            idUsuario=form.cleaned_data['idUsuario']
            usuario = get_object_or_404(Usuario, pk=idUsuario)
            shelf = shelve.open("dataRS.dat")
            Prefs = shelf['Prefs']
            SimItems = shelf['SimItems']
            shelf.close()

            rankings = getRecommendedItems(Prefs, SimItems, usuario.idUsuario)
            recomendadas = rankings[:3]
            peliculas = []
            puntuaciones = []
            for re in recomendadas:
                peliculas.append(Pelicula.objects.get(pk=re[1]))
                puntuaciones.append(re[0])
            items = zip(peliculas, puntuaciones)
    
    return render(request, 'dos_pelis.html', {'form': form, 'items': items, 'usuario': usuario, 'STATIC_URL': settings.STATIC_URL})


def peliculas_similares(request):
    form = BusquedaPeliculaForm()
    items = None
    pelicula = None

    if request.method == 'POST':
        form = BusquedaPeliculaForm(request.POST)

        if form.is_valid():
            idPelicula=form.cleaned_data['idPelicula']
            pelicula = get_object_or_404(Pelicula, pk=idPelicula)
            shelf = shelve.open("dataRS.dat")
            Prefs = shelf['ItemsPrefs']
            shelf.close()

            similares = topMatches(Prefs, int(idPelicula), n = 3)
            peliculas = []
            similaridad = []
            for re in similares:
                peliculas.append(Pelicula.objects.get(pk=re[1]))
                similaridad.append(re[0])
            items = zip(peliculas, similaridad)

    return render(request, 'peliculas_similares.html', {'form': form, 'pelicula': pelicula, 'items': items, 'STATIC_URL': settings.STATIC_URL})


def usuarios_recomendados(request):
    form = BusquedaPeliculaForm()
    items = None
    pelicula = None

    if request.method == 'POST':
        form = BusquedaPeliculaForm(request.POST)

        if form.is_valid():
            idPelicula=form.cleaned_data['idPelicula']
            pelicula = get_object_or_404(Pelicula, pk=idPelicula)
            shelf = shelve.open("dataRS.dat")
            ItemPrefs = shelf['ItemsPrefs']
            shelf.close()
        
            rankings = getRecommendations(ItemPrefs, int(idPelicula))
            recomendadas = rankings[:3]

            usuarios = []
            puntuaciones = []
            for re in recomendadas:
                usuarios.append(Usuario.objects.get(pk=re[1]))
                puntuaciones.append(re[0])
            items = zip(usuarios, puntuaciones)
    
    return render(request, 'recomendar_usuarios_peliculas.html', {'form': form, 'items': items, 'pelicula': pelicula, 'STATIC_URL': settings.STATIC_URL})

