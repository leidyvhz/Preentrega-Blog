# Blog Django

Proyecto web desarrollado con Django para la gestión de un blog.

## Descripción

Este repositorio contiene la estructura completa de un proyecto Django para construir un blog web, cumpliendo con la configuración base del entorno, el manejo de archivos estáticos (CSS e imágenes), plantillas HTML modulares con herencia y el versionado con Git. El proyecto incluye la aplicación principal `posts`.

## Estructura del Proyecto

```text
blog_consola/
├── blog_project/              # Configuración global del proyecto Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── media/                     # Carpeta de almacenamiento para imágenes subidas
│   └── posts/                 # Archivos de imagen asociados a las publicaciones
├── posts/                     # Aplicación principal del blog
│   ├── migrations/            # Historial de migraciones de base de datos
│   ├── static/                # Archivos estáticos
│   │   └── posts/
│   │       └── css/
│   │           └── estilos.css # Hoja de estilos principal
│   │       └── img/
│   ├── templates/             # Plantillas HTML de la aplicación
│   │   └── posts/
│   │       ├── acerca.html
│   │       ├── base.html
│   │       ├── contacto.html
│   │       ├── detalle_post.html
│   │       ├── editar_post.html
│   │       ├── inicio.html
│   │       ├── lista_posts.html
│   │       └── post_form.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py               # Formularios del sistema (ModelForms y Forms)
│   ├── models.py              # Definición de modelos (Post)
│   ├── tests.py
│   ├── urls.py                # Enrutamiento local de la aplicación
│   └── views.py               # Lógica de negocio y vistas de la app
├── .gitignore                 # Archivos excluidos del control de versiones
├── db.sqlite3                 # Base de datos SQLite local
├── manage.py                  # Script de gestión para comandos de Django
├── readme.md                  # Documentación del proyecto
└── requirements.txt           # Dependencias del proyecto Python
```

## Manejo de Imágenes y Archivos Multimedia

El sistema permite a los usuarios adjuntar una imagen al crear o editar una publicación. Su funcionamiento técnico abarca los siguientes componentes:

1. **Modelo de Datos (`models.py`):**
   - El modelo `Post` incluye un campo de tipo `ImageField`:
     ```python
     imagen = models.ImageField(upload_to='posts/', null=True, blank=True)
     ```
   - Esto almacena las imágenes organizadas dentro de la carpeta multimedia configurada.

2. **Configuración en `settings.py`:**
   - Se definen las rutas globales para los archivos multimedia subidos por los usuarios:
     ```python
     MEDIA_URL = '/media/'
     MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
     ```

3. **Enrutamiento Principal (`urls.py`):**
   - Durante el entorno de desarrollo (`DEBUG = True`), se configuran las URLs estáticas para permitir visualizar las imágenes cargadas desde el panel o los formularios:
     ```python
     if settings.DEBUG:
         urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
     ```

4. **Formularios y Vistas (`post_form.html` y `views.py`):**
   - El formulario HTML implementa el atributo `enctype="multipart/form-data"` indispensable para la transmisión de archivos binarios:
     ```html
     <form method="POST" enctype="multipart/form-data">
     ```
   - En la vista, se capturan los archivos mediante `request.FILES` para asociarlos al registro del modelo.

5. **Visualización en Plantillas (`lista_posts.html` y `detalle_post.html`):**
   - Se valida la existencia de una imagen antes de renderizarla usando condicionales de plantilla:
     ```html
     {% if post.imagen %}
         <img src="{{ post.imagen.url }}" alt="{{ post.titulo }}">
     {% endif %}
     ```

## Instalación y Ejecución

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/leidyvhz/Preentrega-Blog.git](https://github.com/leidyvhz/Preentrega-Blog.git)
   cd blog_consola
   ```

2. **Crear el entorno virtual:**
    ```bash
    python -m venv venv
    ```

3. **Activar el entorno virtual:**
    En Windows (PowerShell):
    ```bash
    venv\Scripts\Activate
    ```

    En Linux o macOS:
    ```bash
    source venv/bin/activate
    ```

4. **Instalar las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

5. **Ejecutar el servidor de desarrollo de Django:**
    ```bash
    python manage.py runserver
    ```

6. **Abrir en el navegador:**
    Ingresa a http://127.0.0.1:8000/ para ver el sitio funcionando.