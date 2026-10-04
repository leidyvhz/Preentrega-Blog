def menu_ppal ():
    print("--- MENU DEL BLOG ---")
    print("1. Ver todos los posts")
    print("2. Buscar por titulo")
    print("3. Filtrar por tag")
    print("4. Validar posts")
    print("5. Salir")
    try:
        opcion = int(input("Ingresa el número de la opción a la que deseas acceder: "))
        return opcion
    except ValueError:
        print("Opción no válida, intenta nuevamente.")