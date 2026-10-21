class Autor:
    def __init__(self, nombre, bio, especialidad, redes_sociales):
        self.nombre = nombre
        self.bio = bio
        self.especialidad = especialidad
        self.redes_sociales = redes_sociales

    def convertir_a_diccionario(self):
        return {
            "nombre": self.nombre,
            "bio": self.bio,
            "especialidad": self.especialidad,
            "redes_sociales": self.redes_sociales
        }

    @classmethod
    def convertir_desde_diccionario(autor, diccionario):
        return autor(
            nombre=diccionario.get("nombre", ""),
            bio=diccionario.get("bio", ""),
            especialidad=diccionario.get("especialidad", ""),
            redes_sociales=diccionario.get("redes_sociales", [])
        )


class Post:
    def __init__(self, id, titulo, contenido, autor, tags, estado):
        self.id = id
        self.titulo = titulo
        self.contenido = contenido
        self.autor = autor
        self.tags = tags
        self.estado = estado

    def convertir_a_diccionario(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "contenido": self.contenido,
            "autor": self.autor.convertir_a_diccionario(),
            "tags": self.tags,
            "estado": self.estado
        }

    @classmethod
    def convertir_desde_diccionario(post, diccionario):
        autor_obj = Autor.convertir_desde_diccionario(diccionario.get("autor", {}))
        return post(
            id=diccionario.get("id"),
            titulo=diccionario.get("titulo", ""),
            contenido=diccionario.get("contenido", ""),
            autor=autor_obj,
            tags=diccionario.get("tags", []),
            estado=diccionario.get("estado", "borrador")
        )


class Blog:
    def __init__(self):
        self.posts = []

    def agregar_post(self, post):
        if isinstance(post, Post):
            self.posts.append(post)
            print("Se agregó post correctamente.")

    def listar_posts(self):
        resultado = []
        for post in self.posts:
            resultado.append(f"* Id: {post.id} - Título: {post.titulo} - Autor: {post.autor.nombre} - Estado: [{post.estado}]")
        return resultado

    def buscar_por_titulo(self, palabra):
        palabra_normalizada = palabra.lower().strip()
        encontrados = []
        for post in self.posts:
            if palabra_normalizada in post.titulo.lower():
                encontrados.append(f"Título: {post.titulo} | Autor: {post.autor.nombre}")
        return encontrados if encontrados else ["No se encontraron coincidencias."]

    def filtrar_por_tag(self, tag):
        tag_normalizado = tag.lower().strip()
        encontrados = []
        for post in self.posts:
            tags_normalizados = [t.lower() for t in post.tags]
            if tag_normalizado in tags_normalizados:
                encontrados.append(f"Título: {post.titulo} - Autor: {post.autor.nombre}")
        return encontrados if encontrados else ["No se encontraron posts con esa etiqueta."]

    def obtener_posts_diccionarios(self):
        return [post.convertir_a_diccionario() for post in self.posts]