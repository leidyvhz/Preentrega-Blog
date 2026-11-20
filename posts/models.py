from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50)
    biografia = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to="avatars/", blank=True, null=True)
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="perfil_autor"
    )
    linkweb = models.URLField(max_length=200, blank=True, null=True)

    @property
    def avatar_url(self):
        if self.imagen and hasattr(self.imagen, "url"):
            return self.imagen.url
        try:
            return staticfiles_storage.url("posts/img/foto_perfil_defecto.png")
        except ValueError:
            return f"{settings.STATIC_URL}posts/img/foto_perfil_defecto.png"

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
class Post(models.Model):
    ESTADOS = [("borrador","Borrador"),("publicado","Publicado"),("archivado","Archivado")]
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    #Arreglar aca para que tambien relacionar con el autor
    autor = models.ForeignKey(Autor,on_delete=models.CASCADE,related_name="posts")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="borrador")
    imagen = models.ImageField(upload_to="posts/",blank=True,null=True)
    # Usuarios que guardaron esta publicación como favorita
    favoritos = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name="posts_guardados",blank=True)
   

    class Meta:
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return f"{self.titulo} - {self.autor}"

class Comentario(models.Model):
    contenido = models.TextField()
    fecha = models.DateField(auto_now_add=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comentarios")
    autor = models.ForeignKey(Autor,on_delete=models.CASCADE,null=True,blank=True,related_name="comentarios")
    def __str__(self):
        return f"Comentario en {self.post.titulo}"

class Calificacion(models.Model):

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="calificaciones"
    )

    autor = models.ForeignKey(
        Autor,
        on_delete=models.CASCADE,
        related_name="calificaciones"
    )

    estrellas = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    class Meta:

        constraints = [

            models.UniqueConstraint(
                fields=["post", "autor"],
                name="una_calificacion_por_usuario"
            ),

            models.CheckConstraint(
                condition=models.Q(estrellas__gte=1) &
                          models.Q(estrellas__lte=5),
                name="calificacion_entre_1_y_5"
            )
        ]

class Mensaje(models.Model):
    remitente = models.ForeignKey(Autor,on_delete=models.CASCADE,related_name="mensajes_enviados")
    destinatario = models.ForeignKey(Autor,on_delete=models.CASCADE,related_name="mensajes_recibidos")
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    visto = models.BooleanField(default=False)
    class Meta:
        ordering = ["fecha_envio"]

class Notificacion(models.Model):
    TIPO_CHOICES = [
        ("aprobado", "Post aprobado"),
        ("rechazado", "Post rechazado"),
    ]

    autor = models.ForeignKey(
        Autor,
        on_delete=models.CASCADE,
        related_name="notificaciones"
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notificaciones"
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    mensaje = models.CharField(max_length=255)
    motivo = models.TextField(blank=True, null=True)
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return f"{self.autor} - {self.mensaje}"