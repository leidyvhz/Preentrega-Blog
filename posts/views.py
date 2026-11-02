from django.shortcuts import get_object_or_404, redirect, render
from posts.forms import ContactoForm, PostForm
from .models import Autor, Post

# Create your views here.

# VISTA DEL INICIO EN LA RAIZ
def inicio(request):
    return render(request, 'posts/inicio.html')

def acerca(request):
    return render(request, 'posts/acerca.html')

def lista_posts(request):
    posts = Post.objects.all()
    busqueda = request.GET.get("buscar")
    if busqueda:
        posts = posts.filter(titulo__icontains = busqueda)
    estado = request.GET.get("estado")
    if estado:
        posts= posts.filter(estado=estado)
    orden = request.GET.get("orden","reciente")
    if orden == "antiguo":
        posts = posts.order_by("fecha_creacion")
    else: 
        posts = posts.order_by("-fecha_creacion")
    contexto = {"posts": posts,"busqueda":busqueda,"estado":estado,"orden":orden}
    return render(request,"posts/lista_posts.html", contexto)

def detalle_post(request,id):
    post = get_object_or_404(Post,id=id)
    return render(request,"posts/detalle_post.html",{"post":post})

def post_form(request):
    autores = Autor.objects.all() # Obtenemos los autores registrados
    if request.method == "POST":
        titulo = request.POST.get("titulo")
        contenido = request.POST.get("contenido")
        autor_id = request.POST.get("autor") # Capturamos el ID del autor seleccionado
        estado = request.POST.get("estado")
        imagen = request.FILES.get("imagen")

        autor_obj = Autor.objects.get(id=autor_id) if autor_id else None

        Post.objects.create(
            titulo=titulo,
            contenido=contenido,
            autor=autor_obj,
            estado=estado,
            imagen=imagen
        )
        return redirect("lista_posts")
    return render(request, "posts/post_form.html", {"autores": autores})

def editar_post(request,id):
    post = get_object_or_404(Post,id=id)
    if request.method == "POST":
        post.titulo= request.POST["titulo"]
        post.contenido = request.POST["contenido"]
        post.autor = request.POST["autor"]
        post.estado = request.POST["estado"]
        if "imagen" in request.FILES:
            post.imagen = request.FILES["imagen"]
        post.save()
        return redirect("lista_posts")
    return render(request, "posts/editar_post.html", {"post": post})

def eliminar_post(request,id):
    post = get_object_or_404(Post,id=id)
    if request.method == "POST":
        post.delete()
    return redirect("lista_posts")

def contacto(request):
    if request.method == "POST":
        form = ContactoForm(request.POST)

        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            email = form.cleaned_data["email"]
            asunto = form.cleaned_data["asunto"]
            mensaje = form.cleaned_data["mensaje"]

            return render( request, "posts/contacto.html",{
                "form": ContactoForm(),
                "enviado":True,
                "nombre": nombre
            },)
    else:
        form = ContactoForm()

    return render( request, "posts/contacto.html", {"form": form})

def lista_autores(request):
    autores = Autor.objects.all()
    busqueda = request.GET.get("buscar")
    if busqueda:
        autores = autores.filter(username__icontains = busqueda)
    return render(request,"autores/lista_autores.html",{"autores":autores})

def perfil_autor(request,id):
    autor = get_object_or_404(Autor,id=id)
    publicaciones = autor.publicaciones.all()

    return render(request,"autores/perfil_autor.html",{"autor":autor,"publicaciones":publicaciones})

def crear_autor(request):
    if request.method == "POST":
        nombre = request.POST["nombre"]
        apellido = request.POST["apellido"]
        email = request.POST["email"]
        username = request.POST["username"]
        autor = Autor(nombre=nombre,apellido=apellido,email=email,username=username)
        autor.save()

        return redirect("inicio")
    return render(request,"autores/crear_autor.html")