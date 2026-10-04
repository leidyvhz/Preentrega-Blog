Este proyecto es una aplicación interactiva en consola desarrollada en Python que permite gestionar, consultar y validar las publicaciones (posts) de un blog. Fue estructurado utilizando paquetes y módulos para aplicar buenas prácticas de organización de código.

El programa presenta un menú interactivo en la consola con las siguientes funcionalidades:
1. Ver todos los posts: Muestra la lista de títulos disponibles y sus respectivos autores.
2. Buscar por título: Realiza búsquedas de publicaciones según una palabra clave ingresada por el usuario.
3. Filtrar por tag: Permite filtrar las publicaciones asociadas a una etiqueta o tema específico (ej. Python, SQL).
4. Validar posts: Inspecciona cada publicación para verificar la integridad de su estructura y comprobar si cumple con todas las reglas requeridas (existencia de claves obligatorias, formato de autor, etiquetas y estados válidos).
5. Salir: Finaliza la ejecución de la aplicación.

El proyecto se encuentra organizado modularmente en un paquete interno llamado blog.
blog_consola/
│
├── blog/                      # Paquete principal con la lógica interna
│   ├── __init__.py            # Define el directorio como un paquete Python
│   ├── datos.py               # Contiene los datos estáticos (posts, autores, estados)
│   ├── menu.py                # Contiene la interfaz del menú de opciones
│   ├── operaciones.py         # Lógica para listar, buscar y filtrar publicaciones
│   └── validaciones.py        # Funciones de validación de estructura de los posts
│
├── main.py                    # Punto de entrada principal para ejecutar la aplicación
└── readme.md                  # Documentación del proyecto

Responsabilidad de cada módulo
* main.py: Es el punto de entrada y orquestador del sistema. Importa las funciones y datos de los módulos internos, controla el flujo principal con un ciclo interactivo y ejecuta la opción seleccionada por el usuario.
* blog/datos.py: Actúa como la fuente de información o base de datos simulada. Define los datos de perfil, estados permitidos, conjuntos de etiquetas y la lista general de publicaciones (posts).
* blog/menu.py: Gestiona la interacción con el usuario en pantalla. Muestra el menú de opciones y captura la entrada del teclado con control de errores numéricos.
* blog/operaciones.py: Contiene la lógica de negocio para la búsqueda y filtrado de publicaciones (listar_posts, buscar_por_titulo, filtrar_por_tag).
* blog/validaciones.py: Encargado del control de calidad e integridad de los datos (validar_post). Verifica que las publicaciones contengan los campos obligatorios y los tipos de datos correctos.

El archivo que se debe ejecutar para iniciar el sistema es main.py.