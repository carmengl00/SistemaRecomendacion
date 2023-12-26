from principal.models import Pelicula, Puntuacion
from datetime import datetime

path = "data"

def populateDB():
    (dict_pelis, count) = populate_peliculas()
    punt = populate_puntuaciones(dict_pelis)
    return (count, punt)

def populate_peliculas():
    Pelicula.objects.all().delete()
    lista=[]
    dict = {}
    fileobj = open(path+"\\movies1.txt", "r", encoding="utf8")
    for line in fileobj.readlines():
        rip = line.split('  ')
        if len(rip) != 5:
            continue
        date = None if len(rip[2]) == 0 else datetime.strptime(rip[2].replace('"', ''), '%Y-%m-%d')
        p = Pelicula(
                idPelicula = int(rip[0]), 
                titulo = rip[1], 
                fecha = date, 
                director =rip[3],
                actoresPrincipales = rip[4])
        lista.append(p)
        dict[int(rip[0])] = p
    fileobj.close()
    
    Pelicula.objects.bulk_create(lista)
    return(dict, Pelicula.objects.count())

def populate_puntuaciones(p):
    Puntuacion.objects.all().delete()
    lista=[]
    fileobj = open(path+"\\ratings.csv", "r", encoding="utf8")
    for line in fileobj.readlines():
        rip = line.split(';')
        if len(rip) != 3:
            continue
        peli = int(rip[1])
        print(peli)
        lista.append(Puntuacion(idUsuario = rip[0], idPelicula = p[peli] , puntuacion = rip[2]))
    fileobj.close()
    
    Puntuacion.objects.bulk_create(lista)

    return Puntuacion.objects.count()

        