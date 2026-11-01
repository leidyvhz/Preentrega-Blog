from django.shortcuts import get_object_or_404, redirect, render
from posts.forms import ContactoForm, PostForm
from posts.models import Post

# Create your views here.
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
    if request.method == "POST":
        titulo = request.POST.get("titulo")
        contenido = request.POST.get("contenido")
        autor = request.POST.get("autor")
        estado = request.POST.get("estado")
        imagen = request.FILES.get("imagen")

        Post.objects.create(
            titulo=titulo,
            contenido=contenido,
            autor=autor,
            estado=estado,
            imagen=imagen
        )
        return redirect("lista_posts")
    return render(request,"posts/post_form.html")

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