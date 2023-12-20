from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Ocupacion(models.Model):
    nombre = models.CharField(max_length=50)

class Usuario(models.Model):
    idUsuario = models.AutoField(primary_key=True)
    edad = models.PositiveIntegerField()
    sexo = models.CharField(max_length=1, verbose_name = 'Sexo', help_text='Debe elegir entre M o F', choices=(('M','Masculino'),('F', 'Femenino')))
    ocupacion = models.ForeignKey(Ocupacion, on_delete = models.CASCADE)
    codigoPostal = models.CharField(max_length=6)

class Categoria(models.Model):
    idCategoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

class Pelicula(models.Model):
    idPelicula = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    fechaEstreno = models.DateField(verbose_name='Fecha de Estreno', null=True)
    url = models.URLField()
    categorias = models.ManyToManyField(Categoria)

class Puntuacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete = models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, on_delete = models.CASCADE)
    puntuacion = models.PositiveIntegerField(verbose_name = 'Puntuacion', help_text='Debe elegir entre 1 y 5', validators = [MinValueValidator(0), MaxValueValidator(5)],
                                            choices = ((1, 'Muy mala'), (2, 'Mala'), (3, 'Regular'), (4, 'Buena'), (5, 'Muy buena')))