from blog.datos import estados_post

def validar_post(post):
    if not isinstance(post, dict):
        return False, "El post no es un diccionario válido."
    
    claves_obligatorias = ["id", "titulo", "contenido", "autor", "tags", "estado"]
    for clave in claves_obligatorias:
        if clave not in post:
            return False, f"Falta la clave obligatoria: '{clave}'."

    if not isinstance(post["titulo"], str) or not post["titulo"].strip():
        return False, "El título no puede estar vacío."

    if not isinstance(post["contenido"], str) or not post["contenido"].strip():
        return False, "El contenido no puede estar vacío."

    if not isinstance(post["autor"], dict):
        return False, "El autor debe ser un diccionario."

    if "nombre" not in post["autor"] or not str(post["autor"]["nombre"]).strip():
        return False, "El diccionario de autor no contiene la clave 'nombre'."

    if not isinstance(post["tags"], list):
        return False, "Las etiquetas ('tags') deben ser una lista."

    if post["estado"] not in estados_post:
        return False, f"El estado '{post['estado']}' no es válido. Debe ser uno de: {estados_post}"

    return True, "El post es válido."