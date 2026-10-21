import json
import os
from blog.modelos import Autor, Post, Blog

perfil_autor = {
    "nombre" : "Leidy Herrera",
    "bio" : "Data Analytics",
    "especialidad" : "Python y SQL",
    "redes_sociales" : ["@leidypy", "@leidy_data"]
}

estados_post = ("borrador", "publicado", "archivado")

etiquetas_blog = {"Python", "Django", "Web", "Backend", "Python", "Data Analytics", "Principiante", "SQL"}

posts_iniciales = [
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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_JSON = os.path.join(BASE_DIR, "posts.json")

def cargar_datos_json():
    blog = Blog()
    
    if not os.path.exists(ARCHIVO_JSON):
        guardar_datos_json(posts_iniciales)
    
    try:
        with open(ARCHIVO_JSON, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            if not isinstance(datos, list):
                datos = []
            for item in datos:
                post_obj = Post.convertir_desde_diccionario(item)
                blog.agregar_post(post_obj)
    except (json.JSONDecodeError, Exception):
        print("Advertencia: El archivo posts.json está vacío o dañado. Se inicializará vacío.")
    
    return blog

def guardar_datos_json(posts_data):
    try:
        if isinstance(posts_data, Blog):
            data_a_guardar = posts_data.obtener_posts_diccionarios()
        else:
            data_a_guardar = posts_data
            
        with open(ARCHIVO_JSON, "w", encoding="utf-8") as archivo:
            json.dump(data_a_guardar, archivo, ensure_ascii=False, indent=4)
        return True, "Datos guardados exitosamente en posts.json."
    except Exception as e:
        return False, f"Error al guardar el archivo: {e}"