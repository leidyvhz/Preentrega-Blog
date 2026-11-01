from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["titulo", "contenido", "autor", "estado", "imagen"]

class ContactoForm(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=100)
    email = forms.EmailField(label="Correo Electronico")
    asunto = forms.CharField(label="Asunto", max_length=150)
    mensaje = forms.CharField(label="Mensaje", widget=forms.Textarea)