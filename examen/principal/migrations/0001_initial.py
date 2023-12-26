# Generated by Django 4.2.7 on 2023-12-20 11:58

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pelicula',
            fields=[
                ('idPelicula', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=50)),
                ('fecha', models.DateField(null=True, verbose_name='Fecha')),
                ('director', models.CharField(max_length=50)),
                ('actoresPrincipales', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Puntuacion',
            fields=[
                ('idUsuario', models.AutoField(primary_key=True, serialize=False)),
                ('puntuacion', models.PositiveIntegerField(choices=[(10, '10'), (15, '15'), (20, '20'), (25, '25'), (30, '30'), (35, '35'), (40, '40'), (45, '45'), (50, '50')], help_text='Debe elegir entre 1 y 5', validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(50)], verbose_name='Puntuacion')),
                ('idPelicula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='principal.pelicula')),
            ],
        ),
    ]