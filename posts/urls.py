from posts import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', views.inicio, name="inicio"),
    path('about/', views.acerca, name="acerca"),
    path('posts/', views.lista_posts, name="lista_posts"),
    path('contacto/', views.contacto, name="contacto"),
    path('crear/', views.post_form, name="post_form"),
    path('post/<int:id>/', views.detalle_post, name="detalle_post"),
    path('post/editar/<int:id>/', views.editar_post, name="editar_post"),
    path('post/eliminar/<int:id>/', views.eliminar_post, name="eliminar_post"),
]