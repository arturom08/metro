import requests
import os
import json
from albums import Albums


ALBUM_API_URL = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/albums.json"

albums =  []

album_ids = set()

def guardar_albums():
    global albums
    try:
        with open('albums.txt', 'w') as f:
            unique_albums = {albums.id: album for album in albums}.values()  # Eliminar duplicados por ID
            json.dump([album.__dict__ for album in unique_albums], f, indent=4)
            print("Datos de albums guardados exitosamente")
    except AttributeError:
        print("Los datos de albums no estan cargados.")
    except Exception as e:
        print(f"No se pudo guardar los albums: {e}")


def guardar_albums_desde_api(datos):
    try:
        new_albums = [Albums(d['id'], d['name'], d['description'], d['cover'], d['published'], d['genre'], d['artist'], d['tracklist']) for d in datos]
        #Verificar si los nuevos albunes ya existen en albums.txt
        for new_album in new_albums:
            if new_album not in albums:
                albums.append(new_album)
                album_ids.add(new_album.id)  #AGregar el nuevo id al conjunto de ids

        #Guarda los datos de albums actualizados en albums.txt
            guardar_albums()
    except Exception as e:
        print(f"No se pudo guardar los albumnes desde la API: {e}")

def cargar_album_desde_archivo():
    global albums, album_ids
    try:
        with open('albums.txt', 'r') as f:
            all_albums_datos = json.load(f)
            albums.clear()
            album_ids.clear()
            for albums_datos in all_albums_datos:
                album_id = albums_datos['id']
                if album_id not in album_ids:
                    albums.append(Albums(**albums_datos))
    except FileNotFoundError:
        print("El archivo albums.txt no existe. No se cargaron datos.")
    except Exception as e:
        print(f"No se pudo cargar los datos desde albums.txt: {e}")



def cargar_album_api():
    global albums
    try:
        # Verificar si el archivo albums.txt existe
        if not os.path.exists('albums.txt'):
            response = requests.get(ALBUM_API_URL)
            if response.status_code == 200:
                datos = response.json()
                albums.extend([Albums(d['id'], d['name'], d['description'], d['cover'], d['published'], d['genre'], d['artist'], d['tracklist'] ) for d in datos])
                guardar_albums_desde_api(datos)
            else:
                # Si el archivo existe, cargar datos desde el archivo
                cargar_album_desde_archivo()

                # Luego, cargar albums adicionales desde la API y actualizar la lista de albums
                response = requests.get(ALBUM_API_URL)
                if response.status_code == 200:
                    datos = response.json()
                    guardar_albums_desde_api(datos) #Guarda los nuevos albumes desde la API al txt
    except requests.RequestException as e:
        print(f"Error en la solicitud: {e}")

