from django.shortcuts import get_object_or_404, redirect, render
from .models import Autor, Calificacion, Post
from django.contrib.auth import login,logout
from django.db.models import Avg,Count
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import AutorCreateForm, AutorForm, CalificacionForm, ComentarioForm, ContactoForm, PostForm, RegistroForm

#VISTA DEL INICIO EN LA RAIZ / 
def inicio(request):
    print("USUARIO:",request.user)
    print("AUTENTICADO:",request.user.is_authenticated)
    return render(request, 'posts/inicio.html')


#READ : Listar posts
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

def detalle_post(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    comentarios = post.comentarios.select_related(
        "autor"
    ).order_by("-fecha")
    datos_calificacion = post.calificaciones.aggregate(
        promedio=Avg("estrellas"),
        cantidad= Count("id")
    )
    promedio = datos_calificacion["promedio"] or 0
    cantidad = datos_calificacion["cantidad"]

    estrellas = int(round(promedio))
    calificacion_usuario = None
    if request.user.is_authenticated:
        autor = Autor.objects.filter(
            usuario=request.user
        ).first()
        if autor:
            calificacion_usuario = Calificacion.objects.filter(
                post= post,
                autor=autor
            ).first()

    if calificacion_usuario:
        form_calificacion = CalificacionForm(
            instance = calificacion_usuario
        )
    else:
        form_calificacion = CalificacionForm()
    form_comentario = ComentarioForm()

    context = {
        "post":post,
        "comentarios":comentarios,
        "promedio":promedio,
        "cantidad":cantidad,
        "estrellas":estrellas,
        "calificacion_usuario": calificacion_usuario,
        "form_calificacion" : form_calificacion,
        "form_comentario" :form_comentario
    }

    return render(request,"posts/detalle_post.html",context)

def lista_autores(request):
    autores = Autor.objects.all()
    busqueda = request.GET.get("buscar")
    if busqueda:
        autores = autores.filter(username__icontains = busqueda)
    return render(request,"autores/lista_autores.html",{"autores":autores})


def perfil_autor(request,autor_id):
    autor = get_object_or_404(Autor,id=autor_id)
    posts = autor.posts.all()

    return render(request,"autores/perfil_autor.html",{"autor":autor,"posts":posts})

@login_required
def editar_perfil(request,autor_id):
    autor = get_object_or_404(Autor,id = autor_id)
    if request.method == "POST":
        form = AutorForm(request.POST, request.FILES,instance=autor)
        if form.is_valid():
            form.save()
            return redirect("perfil_autor",autor_id=autor.id)
    else:
            form = AutorForm(instance=autor)
    return render(request,"autores/editar_perfil.html",{ "form":form,"autor":autor})

#CREATE : Crear post
# Reemplaza la función actual 'post_form' por esta:

@login_required
def post_form(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            
            autor_actual = Autor.objects.filter(usuario=request.user).first()
            
            if autor_actual:
                post.autor = autor_actual
                post.save()
                return redirect("lista_posts")
            else:
                form.add_error(None, "Debes tener un perfil de Autor creado antes de poder publicar.")
    else:
        form = PostForm()
    
    return render(request, "posts/post_form.html", {"form": form})




def crear_autor(request):
    if request.method == "POST":
       form = AutorCreateForm(request.POST,request.FILES)
       if form.is_valid():
        form.save()
        return redirect("lista_autores")
    else:
        form = AutorCreateForm()
    return render(request,"autores/post_form.html",{"form":form})

@login_required
def dejar_comentario(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    autor = Autor.objects.filter(usuario=request.user).first()
    
    if request.method == "POST":
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.post = post
            if autor:
                comentario.autor = autor
            comentario.save()
            messages.success(request, "¡Tu comentario se publicó exitosamente!")
            
    return redirect("detalle_post", post_id=post.id)

@login_required
def calificar_post(request,post_id):
    print("ENTRO A CALIFICAR")
    print("METODO:",request.method)
    print("DATOS: " ,request.POST)
    post = get_object_or_404(
        Post,id= post_id
    )
    autor = get_object_or_404(
        Autor,usuario= request.user
    )
    if request.method == "POST":
        form = CalificacionForm(request.POST)
        if form.is_valid():
            estrellas = form.cleaned_data["estrellas"]
            Calificacion.objects.update_or_create(
                post = post,
                autor = autor,
                defaults= {
                    "estrellas" :estrellas
                }
            )
    return redirect("detalle_post",post_id= post.id)


#UPDATE: Actualizar un post
# UPDATE: Actualizar un post
@login_required
def editar_post(request, id):
    post = get_object_or_404(Post, id=id)
    
    if request.method == "POST":
        post.titulo = request.POST["titulo"]
        post.contenido = request.POST["contenido"]
        post.estado = request.POST["estado"]
        
        if "imagen" in request.FILES:
            post.imagen = request.FILES["imagen"]

        post.save()
        return redirect("lista_posts")
    
    return render(request, "posts/editar_post.html", {"post": post})

#DELETE: Eliminar un post
@login_required
def eliminar_post(request,id):
    post = get_object_or_404(Post,id=id)
    if request.method == "POST":
        post.delete()
    return redirect("lista_posts")


#CRUD - Create Read Updete Delete

def contacto(request):
    if request.method == "POST":
        form = ContactoForm(request.POST)

        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            email = form.cleaned_data["email"]
            asunto = form.cleaned_data["asunto"]
            mensaje = form.cleaned_data["mensaje"]

            return render( request, "post/contacto.html",{
                "form": ContactoForm(),
                "enviado":True,
                "nombre": nombre
            },)
    else:
        form = ContactoForm()

    return render( request, "posts/contacto.html", {"form": form})


# -------------------------------
# REGISTRO
# -------------------------------

def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST,request.FILES)
        if form.is_valid():
            usuario = form.save()
            login(request,usuario)
            return redirect("inicio")
    else:
        form = RegistroForm()
    return render(request,"autenticacion/registro.html",{"form":form})

# -------------------------------
# LOGIN
# -------------------------------

def iniciar_sesion(request):
    if request.method == "POST":
        form = AuthenticationForm(request,data =request.POST)

        if form.is_valid():
            usuario = form.get_user()
            login(request,usuario)
            return redirect("inicio")
    
    else:
        form = AuthenticationForm(request)
        
    return render(request,"autenticacion/login.html",{"form":form})


# -------------------------------
# LOGOUT
# -------------------------------

@require_POST

def cerrar_sesion(request):
    logout(request)
    return redirect("inicio")