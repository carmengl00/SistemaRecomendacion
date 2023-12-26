from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Pelicula(models.Model):
    idPelicula = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=50)
    fecha = models.DateField(verbose_name='Fecha', null=True)
    director = models.CharField(max_length=50)
    actoresPrincipales = models.TextField()

class Puntuacion(models.Model):
    idUsuario = models.AutoField(primary_key=True)
    idPelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    puntuacion = models.PositiveIntegerField(verbose_name = 'Puntuacion', help_text='Debe elegir entre 1 y 5', validators = [MinValueValidator(10), MaxValueValidator(50)],
                                            choices = ((10, '10'), (15, '15'), (20, '20'), (25, '25'), (30, '30'), (35, '35'), (40, '40'), (45, '45'), (50, '50')))
    