from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Post, Autor

class PostTestCase(TestCase):
    def setUp(self):
        self.autor = Autor.objects.create(
            nombre="Juan",
            apellido="Perez",
            email="juan@test.com",
            username="juanp"
        )
        self.post = Post.objects.create(
            titulo="Post Original",
            contenido="Contenido de prueba",
            autor=self.autor,
            estado="publicado"
        )

    def test_crear_post_con_imagen(self):
        imagen_falsa = SimpleUploadedFile(
            name='test_image.jpg', 
            content=b'', 
            content_type='image/jpeg'
        )
        data = {
            'titulo': 'Nuevo Post Test',
            'contenido': 'Texto de prueba',
            'autor': self.autor.id,
            'estado': 'borrador',
            'imagen': imagen_falsa
        }
        response = self.client.post(reverse('post_form'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 2)

    def test_editar_post(self):
        data = {
            'titulo': 'Post Modificado',
            'contenido': 'Contenido actualizado',
            'autor': self.autor.id,
            'estado': 'archivado'
        }
        response = self.client.post(reverse('editar_post', args=[self.post.id]), data)
        self.assertEqual(response.status_code, 302)
        
        self.post.refresh_from_db()
        self.assertEqual(self.post.titulo, 'Post Modificado')
        self.assertEqual(self.post.estado, 'archivado')

    def test_eliminar_post(self):
        response = self.client.post(reverse('eliminar_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 0)