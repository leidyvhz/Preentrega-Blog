from django.shortcuts import render

# Create your views here.
def inicio(request):
    return render(request, 'posts/inicio.html')

def acerca(request):
    return render(request, 'posts/acerca.html')

def lista_posts(request):
    return render(request, 'posts/lista_posts.html')

def lista_posts(request):
    posts = [
        {"id": 1, "titulo": "Mi primer post", "autor": "Ana"},
        {"id": 2, "titulo": "Aprendiendo Django", "autor": "Luis"},
        {"id": 3, "titulo": "Rutas y vistas", "autor": "Marta"},
    ]
    contexto = {
        "posts": posts
    }
    return render(request, "posts/lista_posts.html", contexto)