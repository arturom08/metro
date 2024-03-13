import requests
import json
import pickle
import inquirer
import uuid
import os

METROTIFY_API_URL = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/users.json"


class User:
    def __init__(self, id, name, email, username, type):
        self.id = id
        self.name = name
        self.email = email
        self.username = username
        self.type = type

users = []

def generar_id_unique():
    return str(uuid.uuid4())


def guardar_datos():
    global users
    try:
        with open('users.txt', 'w') as f:
            unique_users = {user.id: user for user in users}.values()  # Eliminar duplicados por ID
            json.dump([user.__dict__ for user in unique_users], f, indent=4)
            print("Datos de usuario guardados correctamente")
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
            for user_data in all_users_data:
                user_id = user_data['id']
                if user_id not in user_ids:
                    users.append(User(**user_data))
                    user_ids.add(user_id)
    except FileNotFoundError:
        print("El archivo users.txt no existe. No se cargaron datos.")
    except Exception as e:
        print(f"No se pudo cargar los datos desde users.txt: {e}")





def consultar_todo():
    global users
    if not users:
        print("No hay usuarios cargados")
        return
    print("Lista de usuarios:")
    for user in users:
        print(f"Nombre: {user.name}, Email: {user.email}, Username: {user.username}, Tipo: {user.type}")


if __name__ == "__main__":
    cargar_datos()
    guardar_datos()
        


def mostrar_menu():
    print("Bienvenido a 🎧 Metrotify ♬")
    print("1. Registrar nuevo usuario")
    print("2. Buscar perfiles por nombre")
    print("3. Actualizar información personal")
    print("4. Borrar cuenta")
    print("5. Salir")
    print("6. Consultar todos los usuarios")


def registrar_usuario():
    def validar_pass(password): #Puedo quitar validar_pass por que no estan pidiendo validacion
        # Verificar la longitud mínima de la contraseña
        if len(password) < 8: 
            return False, "La contraseña debe tener al menos 8 caracteres."
        # Verificar si la contraseña contiene al menos un número
        if not any(char.isdigit() for char in password):
            return False, "La contraseña debe contener al menos un número."
        # Verificar si la contraseña contiene al menos un carácter especial
        if not any(char in "!@#$%^&*()-_=+{}[]|;:,.<>?/" for char in password):
            return False, "La contraseña debe contener al menos un carácter especial."
        return True, ""
        
        
    name = input("Ingrese el nombre: ")
    email = input("Ingrese el correo electrónico: ")
    username = input("Ingrese el apodo de usuario: ")

    while True:
        password = input("Ingresa una contraseña: ")
        es_valida, mensaje = validar_pass(password)
        if es_valida:
            confirmar_password = input("Confirme la contraseña: ")
            if password == confirmar_password:
                break
            else:
                print("Las contraseñas no coinciden. Por favor, inténtelo de nuevo.")
                continue
        else:
            print(mensaje)
            continue
    
    type = [
            inquirer.List('size',
                            message="Seleccione el tipo de usuario: ",
                            choices=['musician','listener']
                            )                
    ]
    type_select = inquirer.prompt(type)['size']

    #creamos un dicccionario con los datos del usuario registrado
    id_unique = generar_id_unique()

    user_registered = {
        "id": id_unique,
        "name": name,
        "email": email,
        "username": username,
        "password": password,
        "type": type_select,
    }

    guardar_datos(user_registered)

    print("Usuario registrado exitosamente.")
    print(json.dumps(user_registered, indent=4))

# API_URL = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/users.json"

#Buscar perfiles en el txt

def buscar_perfiles_por_nombre():
    global users

    if not users:
        print("No se han cargado los datos del usuario. intente recargar el prorama")
        return
    
    while True:  
        name = input("Ingrese el nombre para buscar el perfil: ")        

        resultados = [perfil for perfil in users if perfil.name.lower().startswith(name.lower())]
        if resultados:
                print("Resultados de búsqueda: ")
                for perfil in resultados:
                    print(f"Id: {perfil.id}")
                    print(f"Nombre: {perfil.name}")
                    print(f"Email: {perfil.email}")
                    print(f"Username: {perfil.username}")
                    print(f"Tipo: {perfil.type}") 

        print("Submenu 🎧 Metrotify ♬")
        print("1. Volver al menu")
        print("2. Continuar con otra busqueda")
        opcion = input("Seleccione una opción (1-2): ")

        if opcion == "1":
            break
        elif opcion == "2":
            continue
        else:
          print("Opcion invalida. intente nuevamente.")


   
    # Mostrar los perfiles encontrados

def actualizar_informacion_personal():
    id = input("Ingrese el ID del usuario: ")
    name = input("Ingrese el nuevo nombre: ")
    email = input("Ingrese el nuevo correo electrónico: ")
    username = input("Ingrese el apodo de usuario: ")

    # Aquí iría la lógica para actualizar la información personal en la API
    # ...

    print("Información actualizada correctamente.")

def borrar_cuenta():
    id_usuario = input("Ingrese el ID del usuario para borrar la cuenta: ")

    # Aquí iría la lógica para borrar la cuenta en la API
    # ...

    print("Cuenta eliminada correctamente.")



if __name__ == "__main__":
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-5): ")

        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            buscar_perfiles_por_nombre()
        elif opcion == "3":
            actualizar_informacion_personal()
        elif opcion == "4":
            borrar_cuenta()
        elif opcion == "5":
            print("¡Hasta luego!")
            break
        elif opcion == "6":
            consultar_todo()
        else:
            print("Opción inválida. Intente nuevamente.")
