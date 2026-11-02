from posts import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name="inicio"),
    path('about/', views.acerca, name="acerca"),
    path('posts/', views.lista_posts, name="lista_posts"),
    path('contacto/', views.contacto, name="contacto"),
    path('crear/', views.post_form, name="post_form"),
    path('post/<int:id>/', views.detalle_post, name="detalle_post"),
    path('post/editar/<int:id>/', views.editar_post, name="editar_post"),
    path('post/eliminar/<int:id>/', views.eliminar_post, name="eliminar_post"),
    path('autor/crear/',views.crear_autor,name="crear_autor"),
    path('autores/',views.lista_autores,name="lista_autores"),
    path('autor/<int:id>/',views.perfil_autor,name="perfil_autor"),
]