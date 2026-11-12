# Blog Django

Proyecto web desarrollado con Django para la gestión integral de un blog con sistema de usuarios, autores, perfiles, comentarios y publicaciones multimedia.

## Descripción

Este repositorio contiene la estructura completa de un proyecto Django para construir un blog web avanzado. El sistema incluye autenticación de usuarios, vinculación automática de perfiles de autor, subida de imágenes optimizada mediante formularios y vistas protegidas, además de secciones interactivas como comentarios.

## Estructura del Proyecto

```text
blog_project/              # Configuración global del proyecto Django
├── __init__.py
├── asgi.py
├── settings.py
├── urls.py
└── wsgi.py
media/                     # Carpeta de almacenamiento para archivos multimedia
├── avatars/               # Fotos de perfil de los autores
└── posts/                 # Imágenes asociadas a las publicaciones
posts/                     # Aplicación principal del blog
├── migrations/            # Historial de migraciones de base de datos
├── static/                # Archivos estáticos
│   └── posts/
│       └── css/
│           └── estilos.css # Hoja de estilos principal con Flexbox
│       └── img/
├── templates/             # Plantillas HTML de la aplicación
│   ├── autenticacion/     # Vistas de login, registro y cambio de contraseña
│   │   ├── cambiar_contraseña.html
│   │   ├── login.html
│   │   └── registro.html
│   ├── autores/           # Vistas de gestión de perfiles de autor
│   │   ├── crear_autor.html
│   │   ├── editar_perfil.html
│   │   ├── lista_autores.html
│   │   └── perfil_autor.html
│   └── posts/             # Vistas de publicaciones y componentes base
│       ├── base.html
│       ├── contacto.html
│       ├── dejar_comentario.html
│       ├── detalle_post.html
│       ├── editar_post.html
│       ├── eliminar_post.html
│       ├── inicio.html
│       ├── lista_posts.html
│       └── post_form.html
├── __init__.py
├── admin.py               # Configuración del panel de administración
├── apps.py
├── forms.py               # Formularios del sistema (ModelForms y Forms)
├── models.py              # Definición de modelos (Post, Autor, Comentario)
├── tests.py
├── urls.py                # Enrutamiento local de la aplicación
└── views.py               # Lógica de negocio, vistas protegidas y CRUDs
.gitignore                 # Archivos excluidos del control de versiones
db.sqlite3                 # Base de datos SQLite local
manage.py                  # Script de gestión para comandos de Django
readme.md                  # Documentación del proyecto
requirements.txt           # Dependencias del proyecto Python
```

# Documentación del Sistema y Módulos Clave

1. ¿Cómo funciona el registro?
El sistema cuenta con un formulario personalizado llamado RegistroForm que hereda de UserCreationForm.
Proceso: El usuario ingresa sus datos (nombre, apellido, correo, nombre de usuario y contraseña).
Validación y Creación: Una vez que el formulario valida que el correo y el nombre de usuario no estén en uso, se crea el objeto User nativo de Django. Inmediatamente después, se intercepta el método save() para instanciar y asociar de forma automática un registro en el modelo Autor utilizando los mismos datos provistos y el avatar opcional. Al finalizar con éxito, el usuario es autenticado automáticamente y redirigido al inicio.

2. ¿Cómo iniciar sesión?
El inicio de sesión se gestiona a través de la vista iniciar_sesion apoyada en el formulario nativo AuthenticationForm de Django.
Proceso: El usuario navega a la ruta /login/, introduce sus credenciales (username y password).
Autenticación: Si los datos coinciden con un registro válido en la base de datos, la función login(request, usuario) establece la sesión activa en el navegador, permitiendo al usuario acceder a las opciones exclusivas de la plataforma y visualizando su saludo personalizado en el menú de navegación.

3. ¿Cómo cerrar sesión?
El cierre de sesión está configurado mediante la vista cerrar_sesion y protegido con el decorador @require_POST para evitar ataques CSRF mediante peticiones GET accidentales.
Proceso: Al hacer clic en el botón "Cerrar sesión" en la barra de navegación, se ejecuta un formulario con método POST que invoca la función logout(request), destruyendo la sesión activa del usuario y redirigiéndolo de forma segura a la página de inicio.

4. ¿Cómo se creó el modelo Perfil (Autor)?
El modelo Autor actúa como la extensión del perfil de usuario en la aplicación:
Relación: Se conecta al modelo de usuario nativo (User) mediante una relación uno a uno (OneToOneField) utilizando on_delete=models.CASCADE para asegurar la integridad referencial en caso de que la cuenta sea eliminada.
Campos: Almacena información complementaria como nombre, apellido, email, username, un campo ImageField (imagen) para el avatar y la llave foránea hacia User.

5. ¿Cómo se configuran los avatares de perfil?
La gestión y visualización de avatares se compone de los siguientes ajustes:
Almacenamiento: En models.py, el campo de imagen del autor se define con upload_to="avatars/", guardando los archivos subidos dentro de la carpeta multimedia configurada (media/avatars/).
Formularios: Los formularios de registro y edición (RegistroForm y AutorForm) incorporan campos de tipo archivo y se renderizan en las plantillas utilizando el atributo enctype="multipart/form-data".
Visualización: En el archivo base.html y en el perfil de autor, se valida la existencia del avatar mediante condicionales ({% if user.perfil_autor.imagen %}), mostrando la miniatura redondeada optimizada mediante estilos CSS con object-fit: cover.

6. Qué rutas están protegidas
Las rutas que exigen validación de seguridad a nivel de URL y vistas son aquellas asociadas a operaciones de modificación, creación e interacción personal:

/crear/ (Creación de posts)
/editar/<int:id> (Edición de posts)
/eliminar/<int:id> (Eliminación de posts)
/autor/<int:autor_id>/editar (Edición de perfil de autor)
/post/<int:post_id>/comentar (Creación de comentarios)
/cambiar_contraseña/ (Modificación de credenciales)

6. Qué rutas están protegidas
Las rutas que exigen validación de seguridad a nivel de URL y vistas son aquellas asociadas a operaciones de modificación, creación e interacción personal:

/crear/ (Creación de posts)
/editar/<int:id> (Edición de posts)
/eliminar/<int:id> (Eliminación de posts)
/autor/<int:autor_id>/editar (Edición de perfil de autor)
/post/<int:post_id>/comentar (Creación de comentarios)
/cambiar_contraseña/ (Modificación de credenciales)

7. Qué vistas requieren autenticación
Todas las funciones lógicas dentro de views.py encargadas de procesar formularios de creación, actualización o eliminación de datos están blindadas mediante el decorador de control de acceso:
@login_required: Se aplica a las vistas post_form, editar_post, eliminar_post, editar_perfil, dejar_comentario y cerrar_sesion. Si un usuario anónimo intenta acceder directamente a estas vistas o URLs, el sistema lo redirige automáticamente de manera segura hacia la pantalla de inicio de sesión (/login/).

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