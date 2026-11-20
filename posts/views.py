import json
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required , user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Avg, Count,Q
from django.db import models
from django.http import JsonResponse
from .models import Autor, Calificacion, Comentario, Mensaje, Notificacion, Post
from django.views.decorators.http import require_GET, require_POST
from .forms import (
    AutorCreateForm,
    AutorForm,
    CalificacionForm,
    ComentarioForm,
    ContactoForm,
    MensajeForm,
    PostForm,
    RegistroForm
)

# ==========================================
# ADMINISTRADOR
# ==========================================


def es_administrador(user):
    return user.is_staff


@login_required
@user_passes_test(es_administrador)

def posts_pendientes(request):

    posts = Post.objects.filter(estado = "borrador").order_by("-fecha_creacion")
    return render(request,"posts/posts_pendientes.html",{"posts":posts})

@login_required
@user_passes_test(es_administrador)

def revisar_post(request,post_id):
    post = get_object_or_404(Post,id=post_id,estado = "borrador")

    if request.method == "POST":
        accion = request.POST.get("accion")
        if accion == "aprobar":
            post.estado = "publicado"
            post.save()
            if post.autor:
                    Notificacion.objects.create(
                    autor=post.autor,
                    post=post,
                    tipo="aprobado",
                    mensaje=f'Tu post "{post.titulo}" fue aprobado y ya está publicado.'
        )

        elif accion == "rechazar":
            motivo = request.POST.get("motivo_rechazo", "").strip()
            titulo_post = post.titulo
            autor_post = post.autor
            post.estado = "archivado"
            post.save()

            if autor_post:
                Notificacion.objects.create(
                    autor=autor_post,
                    post=post,
                    tipo="rechazado",
                    mensaje=f'Tu post "{titulo_post}" fue rechazado en revisión.',
                    motivo=motivo or None
                )
        
        else: 
            messages.error(request,"Acción no valida")
            return redirect("posts_pendientes")

    print("ESTADO",post.estado)
    return redirect("posts_pendientes")


# ==========================================
# INICIO
# ==========================================

def inicio(request):
    posts_recientes = Post.objects.filter(
        estado="publicado"
    ).order_by("-fecha_creacion")[:3]

    # Obtenemos los últimos cuatro autores registrados

    autores_recientes = Autor.objects.order_by("-id")[:4]

    # Modelo de usuarios configurado en Django
    Usuario = get_user_model()

    # Estadísticas de la comunidad
    total_posts = Post.objects.filter(
        estado="publicado"
    ).count()

    total_autores = Autor.objects.count()

    total_miembros = Usuario.objects.filter(
        is_active=True
    ).count()


    contexto = {
        "posts_recientes": posts_recientes,
        "autores_recientes": autores_recientes,
        # Estadísticas
        "total_posts": total_posts,
        "total_autores": total_autores,
        "total_miembros": total_miembros,
    }

    return render(
        request,
        "posts/inicio.html",
        contexto
    )


# ==========================================
# LISTAR PUBLICACIONES
# ==========================================


from django.db.models import Avg, Count

def lista_posts(request):

    posts = Post.objects.filter(estado="publicado")

    # Buscador por título
    busqueda = request.GET.get("buscar")

    if busqueda:
        posts = posts.filter(
            titulo__icontains=busqueda
        )

    # Ordenar publicaciones
    orden = request.GET.get("orden", "reciente")

    if orden == "antiguo":
        posts = posts.order_by("fecha_creacion")
    else:
        posts = posts.order_by("-fecha_creacion")

    # Calcular promedio y cantidad de calificaciones
    posts = posts.annotate(
        promedio_calificacion=Avg("calificaciones__estrellas"),
        cantidad_calificaciones=Count("calificaciones")
    )

    contexto = {
        "posts": posts,
        "busqueda": busqueda,
        "orden": orden
    }

    return render(
        request,
        "posts/lista_posts.html",
        contexto
    )


# ==========================================
# DETALLE DE UNA PUBLICACIÓN
# ==========================================

def detalle_post(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id
    )

    # Buscamos los comentarios de la publicación
    comentarios = post.comentarios.select_related(
        "autor"
    ).order_by("-fecha")

    # Calculamos el promedio y la cantidad de calificaciones
    datos_calificacion = post.calificaciones.aggregate(
        promedio=Avg("estrellas"),
        cantidad=Count("id")
    )

    promedio = datos_calificacion["promedio"] or 0
    cantidad = datos_calificacion["cantidad"]

    # Redondeamos el promedio para mostrar las estrellas
    estrellas = int(round(promedio))

    # Buscamos si el usuario autenticado ya calificó
    calificacion_usuario = None

    if request.user.is_authenticated:

        autor = Autor.objects.filter(
            usuario=request.user
        ).first()

        if autor:
            calificacion_usuario = Calificacion.objects.filter(
                post=post,
                autor=autor
            ).first()

    # CalificacionForm es un forms.Form, por eso no lleva instance
    form_calificacion = CalificacionForm()

    # Formulario para agregar comentarios
    form_comentario = ComentarioForm()

    contexto = {
        "post": post,
        "comentarios": comentarios,
        "promedio": promedio,
        "cantidad": cantidad,
        "estrellas": estrellas,
        "calificacion_usuario": calificacion_usuario,
        "form_calificacion": form_calificacion,
        "form_comentario": form_comentario
    }

    return render(
        request,
        "posts/detalle_post.html",
        contexto
    )

# ==========================================
# AGREGAR / QUITAR FAVORITOS
# ==========================================

@login_required
def alternar_favorito(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id,
        estado="publicado"
    )

    if post.favoritos.filter(id=request.user.id).exists():

        # Si ya es favorita, la quitamos
        post.favoritos.remove(request.user)

        messages.success(
            request,
            "Post eliminado de favoritos"
        )

    else:

        # Si todavía no es favorita, la agregamos
        post.favoritos.add(request.user)

        messages.success(
            request,
            "Post agregado a favoritos"
        )

    return redirect(
        request.POST.get("next") or "lista_posts"
    )

# ==========================================
# MIS PUBLICACIONES FAVORITAS
# ==========================================

@login_required
def mis_favoritos(request):

    posts_favoritos = request.user.posts_guardados.filter(
        estado="publicado"
    ).select_related("autor")

    contexto = {
        "posts": posts_favoritos
    }

    return render(
        request,
        "posts/mis_favoritos.html",
        contexto
    )



# ==========================================
# LISTAR AUTORES
# ==========================================

def lista_autores(request):

    autores = Autor.objects.all()

    busqueda = request.GET.get("buscar")

    if busqueda:
        autores = autores.filter(
            username__icontains=busqueda
        )

    return render(
        request,
        "autores/lista_autores.html",
        {"autores": autores}
    )


# ==========================================
# PERFIL DE UN AUTOR
# ==========================================

def perfil_autor(request, autor_id):

    autor = get_object_or_404(
        Autor,
        id=autor_id
    )

    posts = autor.posts.all()

    return render(
        request,
        "autores/perfil_autor.html",
        {
            "autor": autor,
            "posts": posts
        }
    )


# ==========================================
# EDITAR PERFIL
# ==========================================

@login_required
def editar_perfil(request, autor_id):

    autor = get_object_or_404(
        Autor,
        id=autor_id
    )

    if request.method == "POST":

        form = AutorForm(
            request.POST,
            request.FILES,
            instance=autor
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Tu perfil fue actualizado correctamente."
            )

            return redirect(
                "perfil_autor",
                autor_id=autor.id
            )

    else:

        form = AutorForm(instance=autor)

    return render(
        request,
        "autores/editar_perfil.html",
        {
            "form": form,
            "autor": autor
        }
    )


# ==========================================
# CREAR PUBLICACIÓN
# ==========================================

@login_required
def post_form(request):

    autor = get_object_or_404(
        Autor,
        usuario=request.user
    )

    # Inicializamos el formulario
    form = PostForm()

    if request.method == "POST":
        form = PostForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            post = form.save(commit=False)

            post.autor = autor
            post.estado = "borrador"

            post.save()

            messages.success(
                request,
                "Tu post está pendiente de aprobación"
            )

            return redirect("lista_posts")

    return render(
        request,
        "posts/post_form.html",
        {"form": form}
    )


# ==========================================
# CREAR AUTOR
# ==========================================

def crear_autor(request):

    if request.method == "POST":

        form = AutorCreateForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect("lista_autores")

    else:

        form = AutorCreateForm()

    return render(
        request,
        "autores/crear_autor.html",
        {"form": form}
    )


# ==========================================
# DEJAR COMENTARIO
# ==========================================

@login_required
def dejar_comentario(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id
    )

    autor = get_object_or_404(
        Autor,
        usuario=request.user
    )

    if request.method == "POST":

        form = ComentarioForm(request.POST)

        if form.is_valid():

            # Creamos el comentario sin guardarlo todavía
            comentario = form.save(commit=False)

            # Asignamos la publicación y el autor
            comentario.post = post
            comentario.autor = autor

            # Guardamos el comentario completo
            comentario.save()

            messages.success(
                request,
                "¡Tu comentario se publicó exitosamente!"
            )

        else:

            messages.error(
                request,
                "No se pudo publicar el comentario."
            )

    return redirect(
        "detalle_post",
        post_id=post.id
    )


# ==========================================
# CALIFICAR PUBLICACIÓN
# ==========================================

@login_required
def calificar_post(request, post_id):

    # Buscamos la publicación
    post = get_object_or_404(
        Post,
        id=post_id
    )

    # Buscamos el perfil del usuario autenticado
    autor = get_object_or_404(
        Autor,
        usuario=request.user
    )

    if request.method == "POST":

        # Recibimos los datos del formulario
        form = CalificacionForm(request.POST)

        if form.is_valid():

            # Convertimos las estrellas a un número entero
            estrellas = int(
                form.cleaned_data["estrellas"]
            )

            print("ESTRELLAS RECIBIDAS:", estrellas)
            print("TIPO:", type(estrellas))

            # Comprobamos que esté entre 1 y 5
            if estrellas < 1 or estrellas > 5:

                messages.error(
                    request,
                    "La calificación debe estar entre 1 y 5."
                )

            else:

                # Creamos o actualizamos la calificación
                calificacion, creada = Calificacion.objects.update_or_create(

                    post=post,

                    autor=autor,

                    defaults={
                        "estrellas": estrellas
                    }
                )

                if creada:

                    messages.success(
                        request,
                        "¡Gracias por calificar esta publicación!"
                    )

                else:

                    messages.success(
                        request,
                        "Tu calificación fue actualizada."
                    )

        else:

            print("ERRORES DEL FORMULARIO:", form.errors)

            messages.error(
                request,
                "No se pudo guardar tu calificación."
            )

    return redirect(
        "detalle_post",
        post_id=post.id
    )


# ==========================================
# EDITAR PUBLICACIÓN
# ==========================================

@login_required

def editar_post(request, id):

    post = get_object_or_404(
        Post,
        id=id,
        autor__usuario = request.user
    )

    if request.method == "POST":

        post.titulo = request.POST["titulo"]
        post.descripcion = request.POST["descripcion"]

        nueva_imagen = request.FILES.get("url_imagen")

        if nueva_imagen:
            post.url_imagen = nueva_imagen

        post.save()

        messages.success(
            request,
            "El post fue actualizado correctamente."
        )

        return redirect("lista_posts")

    return render(
        request,
        "posts/editar_post.html",
        {"post": post}
    )

# ==========================================
# ELIMINAR PUBLICACIÓN
# ==========================================

@login_required
@require_POST
def eliminar_post(request, id):

    post = get_object_or_404(
        Post,
        id=id,
        autor__usuario = request.user
    )



    post.delete()

    messages.success(
            request,
            "El post fue eliminado correctamente."
        )

    return redirect("lista_posts")


# ==========================================
# CONTACTO
# ==========================================

def contacto(request):
    enviado = False
    nombre = ""
    error_envio = None

    if request.method == "POST":
        form = ContactoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data.get("nombre", "")
            email = form.cleaned_data.get("email") or form.cleaned_data.get("correo", "")
            asunto = form.cleaned_data.get("asunto") or "Nuevo mensaje desde el formulario de contacto"
            mensaje = form.cleaned_data.get("mensaje") or form.cleaned_data.get("comentario", "")

            cuerpo_correo = (
                f"Has recibido un nuevo mensaje desde el formulario de contacto de Glups.\n\n"
                f"Nombre: {nombre}\n"
                f"Email: {email}\n"
                f"Asunto: {asunto}\n\n"
                f"Mensaje:\n{mensaje}"
            )

            email_mensaje = EmailMessage(
                subject=f"[Contacto Blog] {asunto}",
                body=cuerpo_correo,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.EMAIL_HOST_USER],
                reply_to=[email] if email else None,
            )

            try:
                email_mensaje.send(fail_silently=False)
                enviado = True
            except Exception as e:
                error_envio = f"No se pudo enviar el mensaje en este momento: {e}"
    else:
        form = ContactoForm()

    return render(
        request,
        "posts/contacto.html",
        {
            "form": form,
            "enviado": enviado,
            "nombre": nombre,
            "error_envio": error_envio,
        },
    )


# ==========================================
# REGISTRO
# ==========================================

def registro(request):

    if request.method == "POST":

        form = RegistroForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            usuario = form.save()

            login(request, usuario)

            autor = get_object_or_404(Autor, usuario=usuario)
            return redirect("editar_perfil", autor_id=autor.id)

    else:

        form = RegistroForm()

    return render(
        request,
        "autenticacion/registro.html",
        {"form": form}
    )


# ==========================================
# INICIAR SESIÓN
# ==========================================

def iniciar_sesion(request):

    if request.method == "POST":

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            usuario = form.get_user()

            login(request, usuario)

            return redirect("inicio")

    else:

        form = AuthenticationForm(request)

    return render(
        request,
        "autenticacion/login.html",
        {"form": form}
    )


# ==========================================
# CERRAR SESIÓN
# ==========================================

@require_POST
def cerrar_sesion(request):

    logout(request)

    return redirect("lista_posts")

# ==========================================
# MENSAJES
# ==========================================
@login_required
def lista_mensajes(request):

    autor_actual = get_object_or_404(
        Autor,
        usuario=request.user
    )

    autores = Autor.objects.exclude(id=autor_actual.id)

    # Mantener la lógica para iniciar una conversación
    if request.method == "GET":
        remitente_id = request.GET.get("remitente")
        destinatario_id = request.GET.get("destinatario")

        if remitente_id and destinatario_id:
            remitente = get_object_or_404(Autor, id=remitente_id)
            destinatario = get_object_or_404(Autor, id=destinatario_id)

            if remitente == autor_actual and remitente != destinatario:
                return redirect(
                    "conversacion",
                    autor1_id=remitente_id,
                    autor2_id=destinatario_id
                )

    # Buscar las conversaciones existentes
    conversaciones = []

    for autor in autores:

        ultimo_mensaje = Mensaje.objects.filter(
            Q(remitente=autor_actual, destinatario=autor) |
            Q(remitente=autor, destinatario=autor_actual)
        ).order_by("-fecha_envio", "-id").first()

        if ultimo_mensaje:

            mensajes_sin_leer = Mensaje.objects.filter(
                remitente=autor,
                destinatario=autor_actual,
                visto=False
            ).count()

            conversaciones.append({
                "autor": autor,
                "ultimo_mensaje": ultimo_mensaje,
                "mensajes_sin_leer": mensajes_sin_leer
            })

    # Ordenar por el mensaje más reciente
    conversaciones.sort(
        key=lambda x: x["ultimo_mensaje"].fecha_envio,
        reverse=True
    )

    return render(
        request,
        "mensajes/lista_mensajes.html",
        {
            "autores": autores,
            "autor_actual": autor_actual,
            "conversaciones": conversaciones
        }
    )

@login_required
def conversacion(request,autor_id):
    autor_actual= get_object_or_404(Autor,usuario = request.user)
    destinatario = get_object_or_404(Autor,id= autor_id)

    if autor_actual == destinatario:
        return redirect("lista_mensajes")

    mensajes = Mensaje.objects.filter(
        models.Q(remitente=autor_actual,destinatario=destinatario)|
        models.Q(remitente=destinatario,destinatario=autor_actual)
    ).order_by("fecha_envio")



    if request.method == "POST":
        contenido = request.POST.get("contenido","").strip()

        if contenido:
            Mensaje.objects.create(
                remitente = autor_actual,
                destinatario= destinatario,
                contenido = contenido
            )
            return redirect("conversacion",autor_id=destinatario.id)
    mensajes.filter(destinatario= autor_actual,visto = False).update(visto = True)
    
    return render(request,"mensajes/conversacion.html",{"autor_actual":autor_actual,"destinatario":destinatario,"mensajes":mensajes})

@login_required
def lista_notificaciones(request):
    autor = Autor.objects.filter(usuario=request.user).first()
    if not autor:
        notificaciones = Notificacion.objects.none()
    else:
        notificaciones = list(Notificacion.objects.filter(autor=autor))
        Notificacion.objects.filter(autor=autor, leida=False).update(leida=True)

    return render(
        request,
        "posts/notificaciones.html",
        {"notificaciones": notificaciones}
    )

def _obtener_autor_actual(request):
    if not request.user.is_authenticated:
        return None
    return Autor.objects.filter(usuario=request.user).first()


@login_required
@require_GET
def mini_chat_resumen(request):
    autor_actual = _obtener_autor_actual(request)
    if not autor_actual:
        return JsonResponse({
            "autores": [],
            "conversaciones": [],
            "total_no_leidos": 0,
        })

    autores = Autor.objects.exclude(id=autor_actual.id).order_by("nombre", "apellido")
    autores_data = [
        {
            "id": a.id,
            "nombre": f"{a.nombre} {a.apellido}".strip() or a.username,
            "username": a.username,
            "avatar_url": a.avatar_url,
        }
        for a in autores
    ]

    mensajes_relacionados = Mensaje.objects.filter(
        Q(remitente=autor_actual) | Q(destinatario=autor_actual)
    ).select_related("remitente", "destinatario").order_by("-fecha_envio")

    conversaciones_map = {}
    for msg in mensajes_relacionados:
        otro = msg.destinatario if msg.remitente == autor_actual else msg.remitente
        if not otro or otro.id == autor_actual.id:
            continue

        if otro.id not in conversaciones_map:
            no_leidos_otro = Mensaje.objects.filter(
                remitente=otro,
                destinatario=autor_actual,
                visto=False
            ).count()
            conversaciones_map[otro.id] = {
                "autor_id": otro.id,
                "nombre": f"{otro.nombre} {otro.apellido}".strip() or otro.username,
                "username": otro.username,
                "avatar_url": otro.avatar_url,
                "ultimo_mensaje": msg.contenido,
                "fecha": msg.fecha_envio.strftime("%d/%m %H:%M"),
                "no_leidos": no_leidos_otro,
            }

    total_no_leidos = Mensaje.objects.filter(
        destinatario=autor_actual,
        visto=False
    ).count()

    return JsonResponse({
        "autores": autores_data,
        "conversaciones": list(conversaciones_map.values()),
        "total_no_leidos": total_no_leidos,
    })


@login_required
@require_GET
def mini_chat_conversacion(request, autor_id):
    autor_actual = _obtener_autor_actual(request)
    if not autor_actual:
        return JsonResponse({"error": "Perfil de autor no encontrado."}, status=400)

    otro_autor = get_object_or_404(Autor, id=autor_id)

    # Marcar como vistos los mensajes que este autor envió al usuario actual
    Mensaje.objects.filter(
        remitente=otro_autor,
        destinatario=autor_actual,
        visto=False
    ).update(visto=True)

    mensajes_qs = Mensaje.objects.filter(
        (Q(remitente=autor_actual) & Q(destinatario=otro_autor)) |
        (Q(remitente=otro_autor) & Q(destinatario=autor_actual))
    ).select_related("remitente", "destinatario").order_by("fecha_envio", "id")

    mensajes_data = [
        {
            "id": m.id,
            "contenido": m.contenido,
            "es_mio": m.remitente_id == autor_actual.id,
            "hora": m.fecha_envio.strftime("%d/%m %H:%M"),
        }
        for m in mensajes_qs
    ]

    total_no_leidos = Mensaje.objects.filter(
        destinatario=autor_actual,
        visto=False
    ).count()

    return JsonResponse({
        "otro_autor": {
            "id": otro_autor.id,
            "nombre": f"{otro_autor.nombre} {otro_autor.apellido}".strip() or otro_autor.username,
            "username": otro_autor.username,
            "avatar_url": otro_autor.avatar_url,
        },
        "mensajes": mensajes_data,
        "total_no_leidos": total_no_leidos,
    })


@login_required
@require_POST
def mini_chat_enviar(request, autor_id):
    autor_actual = _obtener_autor_actual(request)
    if not autor_actual:
        return JsonResponse({"error": "Perfil de autor no encontrado."}, status=400)

    otro_autor = get_object_or_404(Autor, id=autor_id)

    contenido = ""
    if request.content_type and "application/json" in request.content_type:
        try:
            body = json.loads(request.body.decode("utf-8"))
            contenido = (body.get("contenido") or "").strip()
        except (ValueError, UnicodeDecodeError):
            contenido = ""
    else:
        contenido = (request.POST.get("contenido") or "").strip()

    if not contenido:
        return JsonResponse({"error": "El mensaje no puede estar vacío."}, status=400)

    nuevo_mensaje = Mensaje.objects.create(
        remitente=autor_actual,
        destinatario=otro_autor,
        contenido=contenido,
        visto=False,
    )

    return JsonResponse({
        "mensaje": {
            "id": nuevo_mensaje.id,
            "contenido": nuevo_mensaje.contenido,
            "es_mio": True,
            "hora": nuevo_mensaje.fecha_envio.strftime("%d/%m %H:%M"),
        }
    }, status=201)