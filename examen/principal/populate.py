from principal.models import *
from datetime import datetime

path = "data"

def populateDB():
    pass

def populateEsquema():
    '''
    Modelo.objects.all().delete()

    lista=[]
    fileobj = open(path+"\\fichero", "r")
    for line in fileobj.readlines():
        rip = str(line.strip()).split('|')
        if len(rip) != 5:
            continue
        lista.append(Modelo(atributo = tipo(rip[0]), ...))
    fileobj.close()
    Modelo.objects.bulk_create(lista)

    return Modelo.objects.count()
        
    '''

