from django import forms

class BusquedaUsuarioIdForm(forms.Form):
    idUsuario = forms.CharField(label='ID Usuario', widget=forms.TextInput, required=True)

class BusquedaPeliculaForm(forms.Form):
    idPelicula = forms.CharField(label='ID Pelicula', widget=forms.TextInput, required=True)