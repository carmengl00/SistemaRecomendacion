from django import forms

class puntuaciones_usuario_form(forms.Form):
    id_usuario = forms.IntegerField(label='ID Usuario', required=True, min_value=1)