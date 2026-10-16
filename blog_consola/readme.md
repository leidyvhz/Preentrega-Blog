# Aplicación de Consola - Blog en Python (POO y JSON)

Este proyecto es una aplicación interactiva en consola desarrollada en Python que permite gestionar, consultar, validar y persistir las publicaciones (posts) de un blog. Está estructurado aplicando los principios de **Programación Orientada a Objetos (POO)** y buenas prácticas de organización mediante paquetes y módulos.

## Estructura del Proyecto

El proyecto se encuentra organizado modularmente en el paquete interno `blog/`:

* **`main.py`**: Punto de entrada y orquestador del sistema. Controla el flujo principal con un ciclo interactivo y ejecuta las opciones seleccionadas por el usuario.
* **`blog/modelos.py`**: Define las clases del dominio (`Autor`, `Post` y `Blog`), incluyendo sus métodos de negocio (listar, buscar, filtrar) y los métodos de serialización/deserialización para trabajar con diccionarios.
* **`blog/datos.py`**: Encargado de la gestión de datos, conexión con el archivo persistente (`posts.json`) usando rutas absolutas seguras, y carga de datos iniciales.
* **`blog/menu.py`**: Gestiona la interacción visual con el usuario en la consola y captura las opciones del menú principal.
* **`blog/operaciones.py`** *(si aplica)*: Funciones de apoyo secundarias para las operaciones del sistema.
* **`blog/validaciones.py`**: Control de calidad e integridad de los datos, verificando instancias y atributos obligatorios de los posts.
* **`blog/posts.json`**: Archivo local en formato JSON donde se almacenan de manera persistente los posts.

---

## Funcionalidades del Menú Interactivo

1. **Ver todos los posts**: Muestra el identificador, título, autor y estado actual de cada publicación cargada en el blog.
2. **Buscar por título**: Realiza búsquedas de publicaciones según una palabra clave ingresada por el usuario (insensible a mayúsculas/minúsculas).
3. **Filtrar por tag**: Permite filtrar las publicaciones asociadas a una etiqueta o tema específico (ej. *Python*, *SQL*).
4. **Crear nuevo post**: Permite ingresar un nuevo título, contenido, etiquetas y estado para agregarlo al blog y guardarlo automáticamente en el archivo JSON.
5. **Validar posts**: Inspecciona cada publicación para verificar la integridad de su estructura orientada a objetos (instancias correctas, campos no vacíos, estados válidos).
6. **Guardar posts en JSON**: Vuelca y persiste de forma manual el estado actual de los objetos del blog en el archivo JSON.
7. **Salir**: Finaliza la ejecución de la aplicación guardando los datos automáticamente.

---

## Cómo ejecutar el proyecto

Asegúrate de tener instalado **Python** en tu equipo. Ubícate en la carpeta principal del proyecto a través de la terminal y ejecuta el archivo principal:

```bash
python main.py