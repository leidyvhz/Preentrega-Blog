# Blog Django

Proyecto base de un blog web desarrollado con Django.

## Descripción

Este repositorio contiene la estructura inicial de un proyecto Django para construir un blog web, cumpliendo con la configuración base del entorno, el registro de aplicaciones y el versionado con Git. El proyecto incluye una aplicación principal llamada `posts`.

## Estructura del Proyecto

```text
Preentrega-Blog/
├── blog/                      # Módulo de la aplicación de consola
│   ├── __init__.py
│   ├── datos.py
│   ├── menu.py
│   ├── modelos.py
│   ├── operaciones.py
│   ├── posts.json
│   └── validaciones.py
├── blog_project/              # Configuración global del proyecto Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── posts/                     # Aplicación de Django para la gestión del blog
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── .gitignore                 # Archivos excluidos del control de versiones
├── db.sqlite3                 # Base de datos local de Django
├── main.py                    # Punto de entrada para la aplicación en consola
├── manage.py                  # Script de gestión para comandos de Django
├── readme.md                  # Documentación del proyecto
└── requirements.txt           # Dependencias del proyecto Python
```

## Instalación y Ejecución

Clonar el repositorio:
```bash
git clone https://github.com/leidyvhz/Preentrega-Blog.git
```

Entrar a la carpeta del proyecto:
```
cd Preentrega-Blog
```

Crear entorno virtual:
python -m venv venv
Activar entorno virtual:
En Windows PowerShell:
```
.\venv\Scripts\Activate.ps1
```
En Linux o macOS:
```
source venv/bin/activate
```

Instalar dependencias:
```
pip install -r requirements.txt
```

Ejecutar el servidor:
```
python manage.py runserver
```

Abrir en el navegador:
http://127.0.0.1:8000/

Aplicaciones
- posts: aplicación inicial para manejar las publicaciones del blog.