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
├── posts/                     # Aplicación principal del blog
│   ├── migrations/            # Historial de migraciones de base de datos
│   ├── static/                # Archivos estáticos
│   │   └── posts/
│   │       ├── css/
│   │       │   └── estilo.css # Hoja de estilos del proyecto
│   │       └── img/
│   │           └── blog.jpg   # Imágenes del proyecto
│   ├── templates/             # Plantillas HTML de la aplicación
│   │   └── posts/
│   │       ├── acerca.html
│   │       ├── base.html
│   │       ├── inicio.html
│   │       └── lista_posts.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py                # Enrutamiento local de la aplicación
│   └── views.py               # Vistas para renderizar las plantillas
├── .gitignore                 # Archivos excluidos del control de versiones
├── db.sqlite3                 # Base de datos SQLite local
├── manage.py                  # Script de gestión para comandos de Django
├── readme.md                  # Documentación del proyecto
└── requirements.txt           # Dependencias del proyecto Python