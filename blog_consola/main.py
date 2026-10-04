from blog.datos import posts
from blog.menu import menu_ppal
from blog.operaciones import listar_posts
from blog.operaciones import buscar_por_titulo
from blog.operaciones import filtrar_por_tag
from blog.validaciones import validar_post

if __name__ == "__main__":
    while True:
        opcion = menu_ppal()
        if opcion == 1:
            listar_posts(posts)
        elif opcion == 2:
            palabra = input("Ingrese una palabra a buscar: ")
            resultados = []
            resultados = buscar_por_titulo(posts, palabra)
            for resultado in resultados:
                print(resultados)
        elif opcion == 3:
            resultados = []
            tag = input("Ingrese un tag a buscar: ").lower().strip()
            resultados = filtrar_por_tag(posts, tag)
            for resultado in resultados:
                print(resultado)
        elif opcion == 4:
            print("--- RESULTADOS DE VALIDACIÓN ---")
            for idx, post in enumerate(posts, 1):
                es_valido, mensaje = validar_post(post)
                estado_texto = "VÁLIDO" if es_valido else "INVÁLIDO"
                print(f"Post ID {post.get('id', idx)} -> [{estado_texto}]: {mensaje}")
        elif opcion == 5:
            print("Gracias por usar nuestro programa. ¡Hasta luego!")
            break
        else:
            print("No existe esa opción.")