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
            unique_albums = {album.id: album for album in albums}.values()  # Eliminar duplicados por ID
            album_data = []
            for album in unique_albums:
                album_dict = {
                    "id": album.id,
                    "name": album.name,
                    "description": album.description,
                    "cover": album.cover,
                    "published": album.published,
                    "genre": album.genre,
                    "artist": album.artist,
                    "tracklist": []
                }
                for track in album.tracklist:
                    track_dict = {
                        "id": track.id,
                        "name": track.name,
                        "duration": track.duration,
                        "link": track.link
                    }
                    album_dict["tracklist"].append(track_dict)
                album_data.append(album_dict)
            json.dump(album_data, f, indent=4)
            # print("Datos de albums guardados exitosamente")
    except Exception as e:
        print(f"No se pudo guardar los albums: {e}")


def guardar_albums_desde_api(datos):
    try:
        new_albums = [Albums(d['id'], d['name'], d['description'], d['cover'], d['published'], d['genre'], d['artist'], d['tracklist']) for d in datos]
        for new_album in new_albums:
            if new_album not in albums:
                albums.append(new_album)
                album_ids.add(new_album.id)

        guardar_albums()
    except Exception as e:
        print(f"No se pudo guardar los albums desde la API: {e}")


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
        if not albums:
            response = requests.get(ALBUM_API_URL)
            if response.status_code == 200:
                datos = response.json()
                albums.extend([Albums(d['id'], d['name'], d['description'], d['cover'], d['published'], d['genre'], d['artist'], d['tracklist']) for d in datos])
                guardar_albums_desde_api(datos)
            else:
                cargar_album_desde_archivo()
    except requests.RequestException as e:
        print(f"Error en la solicitud: {e}")


