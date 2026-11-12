from django.contrib import admin
from .models import Post, Autor

# 1. Importa también el modelo Autor desde models.py

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "autor",
        "fecha_creacion",
        "estado"
    )

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "nombre",
        "apellido",
        "email"
    )
    search_fields = ("username", "nombre", "email")

admin.site.site_header = "Administracion del Blog"
admin.site.site_title = "Panel del blog"
admin.site.index_title = "Gestion de posts"