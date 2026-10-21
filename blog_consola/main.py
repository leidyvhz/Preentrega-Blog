from blog.datos import cargar_datos_json, guardar_datos_json, estados_post, perfil_autor
from blog.menu import menu_ppal
from blog.validaciones import validar_post
from blog.modelos import Post, Autor

if __name__ == "__main__":
    mi_blog = cargar_datos_json()

    while True:
        opcion = menu_ppal()
        
        if opcion == 1:
            post_disponibles = mi_blog.listar_posts()
            print("\n--- Posts disponibles ---")
            for post in post_disponibles:
                print(post)
            
        elif opcion == 2:
            palabra = input("Ingrese una palabra a buscar en el título: ")
            resultados = mi_blog.buscar_por_titulo(palabra)
            print("\n--- Resultados de Búsqueda ---")
            for resultado in resultados:
                print(resultado)
                
        elif opcion == 3:
            tag = input("Ingrese un tag a buscar: ")
            resultados = mi_blog.filtrar_por_tag(tag)
            print("\n--- Resultados por Etiqueta ---")
            for resultado in resultados:
                print(resultado)
                
        elif opcion == 4:
            print("\n--- CREAR NUEVO POST ---")
            try:
                nuevo_id = len(mi_blog.posts) + 1
                titulo = input("Ingrese el título: ").strip()
                contenido = input("Ingrese el contenido: ").strip()
                tags_input = input("Ingrese tags separados por coma (ej: Python, SQL): ")
                tags = [t.strip() for t in tags_input.split(",") if t.strip()]
                
                print(f"Estados permitidos: {estados_post}")
                estado = input("Ingrese el estado del post: ").strip().lower()
                if estado not in estados_post:
                    estado = "borrador"
                    print("Estado no válido, se asignó 'borrador' por defecto.")

                autor_obj = Autor.convertir_desde_diccionario(perfil_autor)
                nuevo_post = Post(id=nuevo_id, titulo=titulo, contenido=contenido, autor=autor_obj, tags=tags, estado=estado)
                
                mi_blog.agregar_post(nuevo_post)

                exito, mensaje = guardar_datos_json(mi_blog)
                print(f"Post creado con éxito y guardado en JSON: {mensaje}")
            except Exception as e:
                print(f"Error al crear el post: {e}")
                
        elif opcion == 5:
            print("\n--- RESULTADOS DE VALIDACIÓN ---")
            for idx, post in enumerate(mi_blog.posts, 1):
                es_valido, mensaje = validar_post(post)
                estado_texto = "VÁLIDO" if es_valido else "INVÁLIDO"
                print(f"Post ID {post.id} -> [{estado_texto}]: {mensaje}")
                
        elif opcion == 6:
            exito, mensaje = guardar_datos_json(mi_blog)
            print(mensaje)
            
        elif opcion == 7:
            guardar_datos_json(mi_blog)
            print("Gracias por usar nuestro programa. ¡Hasta luego!")
            break
        else:
            print("No existe esa opción, intenta de nuevo.")