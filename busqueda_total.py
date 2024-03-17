import json
from menu import cargar_datos_desde_archivo, submenulist

# Inicialización de la variable global 'users'

users = []

def busqueda_total(user=None, session=None): 
    global users

    # Recargar datos desde el archivo antes de realizar la búsqueda
    cargar_datos_desde_archivo()

    if not users:
        print("No se han cargado los datos del usuario. Intente recargar el programa")
        return
    
    while True:  
        name = input("Ingrese el nombre para buscar: ")        

        # Búsqueda en users.txt
        resultados_users = [perfil for perfil in users if perfil.name.lower().startswith(name.lower())]
        if resultados_users:
            print("Resultados de búsqueda en users.txt: ")
            for perfil in resultados_users:
                print(f"Id: {perfil.id}")
                print(f"Nombre: {perfil.name}")
                print(f"Email: {perfil.email}")
                print(f"Username: {perfil.username}")
                print(f"Tipo: {perfil.type}") 

                perfil_select = perfil

            # Mostrar el submenú si se encontró un perfil
            submenulist(perfil_select, user, session)

        # Búsqueda en albums.txt
        with open('albums.txt', 'r') as f:
            albums = json.load(f)
        resultados_albums = [album for album in albums if album['name'].lower().startswith(name.lower())]
        if resultados_albums:
            print("Resultados de búsqueda en albums.txt: ")
            for album in resultados_albums:
                print(f"Id: {album['id']}")
                print(f"Nombre: {album['name']}")
                print(f"Género: {album['genre']}")

        # Búsqueda en playlist.txt
        with open('playlist.txt', 'r') as f:
            playlists = f.readlines()
        resultados_playlists = [playlist for playlist in playlists if name.lower() in playlist.lower()]
        if resultados_playlists:
            print("Resultados de búsqueda en playlist.txt: ")
            for playlist in resultados_playlists:
                print(playlist)

        if not resultados_users and not resultados_albums and not resultados_playlists:
            print("No se encontraron resultados para la búsqueda.")
