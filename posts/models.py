from django.db import models
from django.utils.text import slugify

# Create your models here.

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50)

    def __str__(self):
        #return self.titulo
        return f"{self.nombre} - {self.apellido}"
    
class Post(models.Model):
    ESTADOS = [("borrador","Borrador"),("publicado","Publicado"),("archivado","Archivado")]
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, null=True, blank=True) # <-- Modificado aquí
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="borrador")
    imagen = models.ImageField(upload_to='posts/', null=True, blank=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True, null=True)
    # ... resto del modelo ...

    class Meta:
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)