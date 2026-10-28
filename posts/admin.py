from django.contrib import admin

# Register your models here.
from .models import Post

@admin.register(Post)

class PostAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "autor",
        "fecha_creacion",
        "estado"
    )

admin.site.site_header = "Administracion del Blog"
admin.site.site_title = "Panel del blog"
admin.site.index_title = "Gestion de posts"