from posts import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', views.inicio, name="inicio"),
    path('about/', views.acerca, name="acerca"),
    path('posts/', views.lista_posts, name="lista_posts"),
]