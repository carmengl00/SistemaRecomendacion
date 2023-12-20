from django.contrib import admin
from principal.models import Ocupacion, Usuario, Categoria, Pelicula, Puntuacion

# Register your models here.
admin.site.register(Ocupacion)
admin.site.register(Usuario)
admin.site.register(Categoria)
admin.site.register(Pelicula)
admin.site.register(Puntuacion)