# Blog Django

Proyecto web desarrollado con Django para la gestión integral de un blog con sistema de usuarios, autores, perfiles, comentarios y publicaciones multimedia.

## Descripción

Este repositorio contiene la estructura completa de un proyecto Django para construir un blog web avanzado. El sistema incluye autenticación de usuarios, vinculación automática de perfiles de autor, subida de imágenes optimizada mediante formularios y vistas protegidas, además de secciones interactivas como comentarios.

## Estructura del Proyecto

```text
blog_consola/
├── blog_project/              # Configuración global del proyecto Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── media/                     # Carpeta de almacenamiento para archivos multimedia
│   ├── avatars/               # Fotos de perfil de los autores
│   └── posts/                 # Imágenes asociadas a las publicaciones
├── posts/                     # Aplicación principal del blog
│   ├── migrations/            # Historial de migraciones de base de datos
│   ├── static/
│   │   └── posts/             # Archivos estáticos de la aplicación
│   │       ├── css/
│   │       │   └── estilos.css # Hoja de estilos principal
│   │       └── img/
│   ├── templates/             # Plantillas HTML de la aplicación
│   │   ├── autenticacion/     # Login, registro, cambio y recuperación de contraseña
│   │   │   ├── cambiar_contraseña.html
│   │   │   ├── login.html
│   │   │   ├── password_reset_complete.html
│   │   │   ├── password_reset_confirm.html
│   │   │   ├── password_reset_done.html
│   │   │   ├── password_reset_email.html
│   │   │   ├── password_reset_subject.txt
│   │   │   ├── password_reset.html
│   │   │   └── registro.html
│   │   ├── autores/           # Vistas de gestión de perfiles de autor
│   │   │   ├── crear_autor.html
│   │   │   ├── editar_perfil.html
│   │   │   ├── lista_autores.html
│   │   │   └── perfil_autor.html
│   │   ├── mensajes/          # Vistas de conversaciones y mensajería
│   │   │   ├── conversacion.html
│   │   │   └── lista_mensajes.html
│   │   └── posts/             # Vistas de publicaciones, moderación, contacto y base
│   │       ├── base.html
│   │       ├── contacto.html
│   │       ├── dejar_comentario.html
│   │       ├── detalle_post.html
│   │       ├── editar_post.html
│   │       ├── eliminar_post.html
│   │       ├── inicio.html
│   │       ├── lista_posts.html
│   │       ├── mis_favoritos.html
│   │       ├── notificaciones.html
│   │       ├── post_form.html
│   │       └── posts_pendientes.html
│   ├── __init__.py
│   ├── admin.py               # Configuración del panel de administración
│   ├── apps.py
│   ├── context_processors.py  # Contadores globales (notificaciones, mensajes, etc.)
│   ├── forms.py               # Formularios del sistema (ModelForms y Forms)
│   ├── models.py              # Definición de modelos (Post, Autor, Comentario, Notificacion, Mensaje, etc.)
│   ├── tests.py
│   ├── urls.py                # Enrutamiento local de la aplicación
│   └── views.py               # Lógica de negocio, vistas protegidas, moderación, chat y CRUDs
├── .gitignore                 # Archivos excluidos del control de versiones
├── db.sqlite3                 # Base de datos SQLite local
├── manage.py                  # Script de gestión para comandos de Django
├── readme.md                  # Documentación del proyecto
└── requirements.txt           # Dependencias del proyecto Python
```

# Instalación y Ejecución

1. Clonar el repositorio:

``` bash
git clone https://github.com/leidyvhz/Preentrega-Blog.git
cd blog_consola
```

2. Crear y activar el entorno virtual:
 - En Windows (PowerShell):

``` bash
python -m venv venv
venv\Scripts\Activate
```

 - En Linux o macOS:
 ``` bash
source venv/bin/activate
 ```

3. Instalar las dependencias:

``` bash
pip install -r requirements.txt
```

4. Aplicar migraciones:

``` bash
python manage.py makemigrations
python manage.py migrate
```

5. Crear un superusuario (para el panel de administración):
``` bash
python manage.py createsuperuser
```

6. Ejecutar el servidor de desarrollo:
``` bash
python manage.py runserver
```

7. Abrir en el navegador:
Ingresa a http://127.0.0.1:8000/ para explorar la plataforma.