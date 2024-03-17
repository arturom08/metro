import requests
import json
import os
from user import User

METROTIFY_API_URL = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/users.json"

users = []

def guardar_datos():
    global users
    try:
        with open('users.txt', 'w') as f:
            unique_users = {user.id: user for user in users}.values()  # Eliminar duplicados por ID
            json.dump([user.__dict__ for user in unique_users], f, indent=4)
            # print("Datos de usuario guardados correctamente")
    except AttributeError:
        print("Los datos de los usuarios no están cargados.")
    except Exception as e:
        print(f"No se pudo guardar los datos: {e}")

# Inicializar conjunto de identificadores de usuario
user_ids = set()

def guardar_datos_desde_api(data):
    global users, user_ids
    try:
        new_users = [User(d['id'], d['name'], d['email'], d['username'], d['type']) for d in data]

        # Verificar si los nuevos usuarios ya existen en users.txt
        for new_user in new_users:
            if new_user not in users:
                users.append(new_user)
                user_ids.add(new_user.id)  # Agregar el nuevo ID al conjunto de IDs

        # Guardar los datos actualizados en users.txt
        guardar_datos()
    except Exception as e:
        print(f"No se pudo guardar los datos desde la API: {e}")

def cargar_datos():
    global users
    try:
        # Verificar si el archivo users.txt existe
        if not os.path.exists('users.txt'):
            # Si el archivo no existe, cargar todos los datos desde la API
            response = requests.get(METROTIFY_API_URL)
            if response.status_code == 200:
                data = response.json()
                users.extend([User(d['id'], d['name'], d['email'], d['username'], d['type']) for d in data])
                guardar_datos_desde_api(data)  # Guardar los datos desde la API
        else:
            # Si el archivo existe, cargar datos desde el archivo
            cargar_datos_desde_archivo()

            # Luego, cargar datos adicionales desde la API y actualizar la lista de usuarios
            response = requests.get(METROTIFY_API_URL)
            if response.status_code == 200:
                data = response.json()
                guardar_datos_desde_api(data)  # Guardar los nuevos datos desde la API
    except requests.RequestException as e:
        print(f"Error en la solicitud: {e}")


def cargar_datos_desde_archivo():
    global users, user_ids
    try:
        with open('users.txt', 'r') as f:
            all_users_data = json.load(f)
            users.clear()
            user_ids.clear()
            for user_data in all_users_data:
                user_id = user_data['id']
                if user_id not in user_ids:
                    if 'password' in user_data:
                        users.append(User(**user_data))
                    else:
                        users.append(User(**user_data, password=None))
                    user_ids.add(user_id)
    except FileNotFoundError:
        print("El archivo users.txt no existe. No se cargaron datos.")
    except Exception as e:
        print(f"No se pudo cargar los datos desde users.txt: {e}")
