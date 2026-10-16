from blog.datos import estados_post
from blog.modelos import Post

def validar_post(post):
    if not isinstance(post, Post):
        return False, "El elemento no es una instancia válida de Post."
    
    if not post.titulo or not str(post.titulo).strip():
        return False, "El título no puede estar vacío."

    if not post.contenido or not str(post.contenido).strip():
        return False, "El contenido no puede estar vacío."

    if not post.autor or not str(post.autor.nombre).strip():
        return False, "El autor debe tener un nombre válido."

    if not isinstance(post.tags, list) or len(post.tags) == 0:
        return False, "Las etiquetas ('tags') deben ser una lista no vacía."

    if post.estado not in estados_post:
        return False, f"El estado '{post.estado}' no es válido. Debe ser uno de: {estados_post}"

    return True, "El post es válido."