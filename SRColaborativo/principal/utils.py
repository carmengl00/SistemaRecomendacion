from principal.models import Puntuacion

def getPuntuacionesUsuario(id_usuario):
    puntuaciones = Puntuacion.objects.filter(usuario_id=id_usuario).values('pelicula_id', 'puntuacion')
    dict_puntuaciones = {}
    for puntuacion in puntuaciones:
        dict_puntuaciones[puntuacion['pelicula_id']] = puntuacion['puntuacion']
    return dict_puntuaciones