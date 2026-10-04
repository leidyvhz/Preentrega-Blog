perfil_autor = {
    "nombre" : "Leidy Herrera",
    "bio" : "Data Analytics",
    "especialidad" : "Python y SQL",
    "redes_sociales" : ["@leidypy", "@leidy_data"]
}

estados_post = ("borrador", "publicado", "archivado")

etiquetas_blog = {"Python", "Django", "Web", "Backend", "Python", "Data Analytics", "Principiante", "SQL"}

posts = [
    {
        "id" : 1,
        "titulo" : "Primeros pasos en el Data Analtylics",
        "contenido" : "Vamos a ver lo que debes tener en cuenta para iniciar en el Data Analytics",
        "autor" : perfil_autor,
        "tags" : ["Principiante", "SQL"],
        "estado" : estados_post[1]
    },
    {
        "id" : 2,
        "titulo" : "¿Cómo descargar e instalar PostgreSQL?",
        "contenido" : "Vamos a ingresar en la web oficial para descargar e instalar el aplicativo PostgreSQL",
        "autor" : perfil_autor,
        "tags" : ["SQL", "Data Bases"],
        "estado" : estados_post[0]
    },
    {
        "id" : 3,
        "titulo" : "Fundamentos en Python",
        "" : "Vamos a ver cómo empezar con Python",
        "autor" : perfil_autor,
        "tags" : ["Python", "Principiante"],
        "estado" : estados_post[2]
    },
    {
        "id" : 4,
        "titulo" : "",
        "contenido" : "Vamos a aprender a crear funciones en Python",
        "autor" : perfil_autor,
        "tags" : ["Python", "Principiante", "Programación"],
        "estado" : estados_post[1]
    }
]