from django.contrib import admin
from django.urls import path, reverse_lazy
from posts import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('posts/', views.lista_posts, name='lista_posts'),
    path('post/<int:post_id>',views.detalle_post, name= "detalle_post"),
    path('crear/', views.post_form, name="post_form"),
    path('editar/<int:id>',views.editar_post, name= "editar_post"),
    path('eliminar/<int:id>',views.eliminar_post, name="eliminar_post"),
    path('autor/crear/',views.crear_autor,name="crear_autor"),
    path('autores/',views.lista_autores,name="lista_autores"),
    path('autor/<int:autor_id>/',views.perfil_autor,name="perfil_autor"),
    path('autor/<int:autor_id>/editar',views.editar_perfil,name="editar_perfil"),
    path("contacto/", views.contacto, name="contacto"),
    path('post/<int:post_id>/comentar',views.dejar_comentario, name= "dejar_comentario"),
    path("post/<int:post_id>/calificar",views.calificar_post,name="calificar_post"),
    path('registro/',views.registro, name="registro"),
    path('login/',views.iniciar_sesion, name="login"),
    path('logout/',views.cerrar_sesion, name="logout"),
    path('cambiar_contraseña/',auth_views.PasswordChangeView.as_view(template_name= "autenticacion/cambiar_contraseña.html",
                                                                     success_url = reverse_lazy("login")),name="cambiar_contraseña"),
    path('posts_pendientes/',views.posts_pendientes,name="posts_pendientes"),
    path('revisar_post/<int:post_id>',views.revisar_post,name="revisar_post"),
        path("mensajes/",views.lista_mensajes,name="lista_mensajes"),
    path("chat/<int:autor_id>",views.conversacion,name="conversacion"),
    path(
    "post/<int:post_id>/favorito/",
    views.alternar_favorito,
    name="alternar_favorito"
        ),
    path(
    "mis-favoritos/",
    views.mis_favoritos,
    name="mis_favoritos"
    ),
    path("notificaciones/", views.lista_notificaciones, name="lista_notificaciones"),
    path("api/mini-chat/resumen/", views.mini_chat_resumen, name="mini_chat_resumen"),
    path("api/mini-chat/conversacion/<int:autor_id>/", views.mini_chat_conversacion, name="mini_chat_conversacion"),
    path("api/mini-chat/enviar/<int:autor_id>/", views.mini_chat_enviar, name="mini_chat_enviar"),
    path(
        "recuperar-password/",
        auth_views.PasswordResetView.as_view(
            template_name="autenticacion/password_reset.html",
            email_template_name="autenticacion/password_reset_email.html",
            subject_template_name="autenticacion/password_reset_subject.txt",
            success_url="/recuperar-password/enviado/",
        ),
        name="password_reset",
    ),
    path(
        "recuperar-password/enviado/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="autenticacion/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "recuperar-password/confirmar/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="autenticacion/password_reset_confirm.html",
            success_url="/recuperar-password/completado/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "recuperar-password/completado/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="autenticacion/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)