def listar_posts(posts):
    print("Posts disponibles: ")
    for post in posts:
        print(f"* {post['titulo']} - Autor: {post['autor']['nombre']}")

def buscar_por_titulo(posts, palabra):
    palabra_normalizada = palabra.lower().strip()
    titulos_encontrados = []
    for post in posts:
        if palabra_normalizada in post["titulo"].lower():
            titulos_encontrados.append(f"Título encontrado: {post['titulo']} | Autor: {post['autor']['nombre']}")
    if titulos_encontrados:
        return titulos_encontrados
    else:
        return ["No se encontraron coincidencias."]

def filtrar_por_tag(posts, tag):
    tags_encontrados = []
    for post in posts:
        tags_normalizados = [etiqueta.lower() for etiqueta in post["tags"]]
        if tag in tags_normalizados:
            tags_encontrados.append(f"Título encontrado: {post['titulo']} - Autor: {post['autor']['nombre']}")
    if tags_encontrados:
        return tags_encontrados
    else:
        return "No se encontraron posts con esa etiqueta."