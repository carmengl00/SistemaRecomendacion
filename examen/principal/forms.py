from django import forms
from .models import *

class ActoresForm(forms.Form):
    actores = ()
    for p in Pelicula.objects.all():
        aux = ()
        rip = p.actoresPrincipales.split(',')
        aux += (r for r in rip if r not in actores)
        actores += (aux,)
    opciones = [(a,a) for a in actores]
    forms.ChoiceField(label='Actor', choices=opciones)