import requests
import json
import inquirer
import uuid
import os
import getpass
from datetime import datetime
import pytz
from albums import Albums
from user import User
from sessions import Session
from list_albums import cargar_album_api, guardar_albums, registrar_album_nuevo
from playclass import MediaPlayer





METROTIFY_API_URL = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/users.json"



users = []

def generar_id_unique():
    return str(uuid.uuid4())

def generar_id_album():
    unique_id = generar_id_unique()
    
    # Formatea el UUID como b48bf9e9-cff4-4313-a61f-4d39b9a40ce2
    album_id = f"{unique_id[0:8]}-{unique_id[9:13]}-{unique_id[14:18]}-{unique_id[19:23]}-{unique_id[24:]}"
    
    return album_id


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



def iniciar_sesion_menu(user=None):
    user = None
    while not user:
        email = input("Ingrese el nuevo correo electrónico: ")
        password = input("Ingresa la contraseña: ")
        
        # Obtener el usuario y el token utilizando la función iniciar_sesion
        user, token = Session.iniciar_sesion(email, password)
    
        if user and token:
            session = Session(user, token)  # Crear una instancia de Session con el usuario y el token
            print("¡Inicio de sesión exitoso!")
            # Aquí puedes hacer lo que necesites con la sesión
        else:
            print("Correo electrónico o contraseña incorrectos.")
            print("Por favor, inténtelo de nuevo.")
    usuarios(user, session) 


def usuarios(user=None, session=None):
    while True:
        if user:
            print(f"👤 Metrotify, {user.name} ")
        else:
            print("👤 Metrotify ")

        questions = [
            inquirer.List(
                "selected_option",
                message="Seleccione una opción:",
                choices=[
                    "Iniciar sesión",
                    "Registrar nuevo usuario",
                    "Actualizar información personal",
                    "Borrar cuenta",
                    "Cerrar sesión",
                    "Regresar al menú"
                ],
            )
        ]

        answers = inquirer.prompt(questions)
        selected_option = answers["selected_option"]

        if selected_option == "Iniciar sesión":
            iniciar_sesion_menu()
        elif selected_option == "Registrar nuevo usuario":
            registrar_usuario()
        elif selected_option == "Actualizar información personal":
            actualizar_informacion_personal(user)
        elif selected_option == "Borrar cuenta":
            borrar_cuenta(user, session)
        elif selected_option == "Regresar al menú":
            mostrar_menu(user, session)
        elif selected_option == "Cerrar sesión":
            cerrar_sesion(session)
            break
        else:
            print("Opción inválida. Intente nuevamente.")


def mostrar_menu(user=None, session=None):
    while True: 
        if user:
            print(f"Bienvenido a 🎧 Metrotify, {user.name} ♬")
        else:
            print("Bienvenido a 🎧 Metrotify ♬")
           
        questions = [
            inquirer.List('option',
                        message="Seleccione una opción:",
                        choices=[
                            ("Usuario"),
                            ("Buscar perfiles por nombre"),
                            ("Gestión musical"),
                            ("Actualizar información personal"),
                            ("Borrar cuenta"),
                            ("Cerrar sesión"),
                        ],
                        ),
        ]
        answer = inquirer.prompt(questions)
        selected_option = answer['option']

        # Lógica para dirigir la selección a las funciones correspondientes        
        if selected_option == "Usuario":
            usuarios(user, session)
        if selected_option == "Buscar perfiles por nombre":
            buscar_perfiles_por_nombre(user, session)
        if selected_option == "Gestión musical":
            menu_musical(user, session)
        if selected_option == "Actualizar información personal":
            actualizar_informacion_personal(user)
        if selected_option == "Borrar cuenta":
            borrar_cuenta(user, session)
        elif selected_option == "Cerrar sesión":
            cerrar_sesion(session)
            break
        else: 
            print("Opción inválida. Intente nuevamente.")

def menu_musical(user=None, session=None):
    while True:
        if user:
            print(f"💽 Metrotify, {user.name} ")
        else:
            print("💽 Metrotify ")

        questions = [
            inquirer.List(
                "selected_option",
                message="Seleccione una opción:",
                choices=[
                    "Crear un álbum",
                    "Buscar musica",
                    "Crear Playlist",
                    "Regresar al menú"
                ],
            )
        ]

        answers = inquirer.prompt(questions)
        selected_option = answers["selected_option"]

        if selected_option == "Crear un álbum":
            registrar_album(user)
        if selected_option == "Buscar musica":
            registrar_usuario()
        if selected_option == "Crear Playlist":
            actualizar_informacion_personal(user)
        elif selected_option == "Regresar al menú":
            mostrar_menu(user, session)
        else:
            print("Opción inválida. Intente nuevamente.")
    

def registrar_album(user=None, session=None):
    
    if user and user.type == "musician":
        print(f"Registre su album 🎧 {user.name} {user.type} ♬")
    elif user.type == "listener":
        print("No tiene los permmisos de músico.")
        mostrar_menu(user, session)
    else:
        print("El usuario no está logueado o no es un músico.")
        mostrar_menu(user, session)
    
    id = generar_id_album()
    print("El id del album es: ", id)
    
    # Obtén la fecha y hora actual en UTC
    ahora = datetime.now(pytz.utc)
    # Formatea la fecha y hora como una cadena de texto en el formato deseado
    fecha_str = ahora.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    
    name = input("Ingrese el nombre del álbum: ")
    description = input("Ingrese la descripción del álbum: ")
    cover = input("Ingrese la URL de la portada del álbum: ")
    published = fecha_str
    print("Fecha de publicación del álbum: ", fecha_str)
    input("Presione Enter para continuar...")
    genre = input("Ingrese el género del álbum: ")
    # artist = input("Ingrese el ID del artista: ")
    artist = user.id
    print("el id del artista es: ", artist)

    tracklist = []
    while True:
        add_track = input("¿Desea agregar una pista al álbum? (s/n): ")
        if add_track.lower() == 'n':
            break

        track_id = generar_id_album()
        print("El id de la musica es: ", id)
        track_name = input("Ingrese el nombre de la pista: ")
        track_duration = input("Ingrese la duración de la pista (MM:SS): ")
        track_link = input("Ingrese el enlace de la pista: ")

        track = {
            "id": track_id,
            "name": track_name,
            "duration": track_duration,
            "link": track_link
        }
        tracklist.append(track)

    album = {
        "id": id,
        "name": name,
        "description": description,
        "cover": cover,
        "published": published,
        "genre": genre,
        "artist": artist,
        "tracklist": tracklist
    }

    registrar_album_nuevo(album)

    print("Álbum registrado exitosamente.")
    print(json.dumps(album, indent=4))
    
    


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

    registrar_nuevo(user_registered)

    print("Usuario registrado exitosamente.")
    print(json.dumps(user_registered, indent=4))


#funcion registrar nuevos usuarios
def registrar_nuevo(user_data):
    try:
        # Verificar si el archivo users.txt existe
        if not os.path.exists('users.txt'):
            # Si el archivo no existe, crearlo y agregar el nuevo usuario
            with open('users.txt', 'w1') as f:
                json.dump([user_data], f, indent=4)
                f.write('\n')
                
        else:
            # Si el archivo existe, abrirlo para agregar el nuevo usuario
            with open('users.txt', 'r+') as f:
                # Cargar los datos actuales del archivo
                users = json.load(f)
                
                # Agregar el nuevo usuario a la lista de usuarios
                users.append(user_data)
                
                # Regresar al principio del archivo
                f.seek(0)
                
                # Escribir la lista de usuarios actualizada en el archivo
                json.dump(users, f, indent=4)
                f.truncate()        
        print("Datos de usuario guardados correctamente")
    except Exception as e:
        print(f"No se pudo guardar los datos: {e}")


def buscar_perfiles_por_nombre(user=None, session=None):
    global users

    # Recargar datos desde el archivo antes de realizar la búsqueda
    cargar_datos_desde_archivo()

    if not users:
        print("No se han cargado los datos del usuario. Intente recargar el programa")
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

                perfil_select = perfil

            # Mostrar el submenú si se encontró un perfil
            submenulist(perfil_select, user, session)

        else:
            print("No se encontraron resultados para la búsqueda.")


def submenulist(perfil_select=None, user=None, session=None):
    print("Submenu 🎧 Metrotify ♬" )
    menu_a = ""
    if perfil_select.type == "listener":
        menu_a = "Submenu Álbumes"
    elif perfil_select.type == "musician":
        menu_a = "Submenu Álbumes"
    else:
        print("Opción inválida. Intente nuevamente.")
        return

    questions = [
        inquirer.List('option',
                      message="Seleccione una opción:",
                      choices=[
                          "Volver al menú",
                          "Continuar con otra búsqueda",
                          menu_a,
                      ],
                      ),
    ]
    answer = inquirer.prompt(questions)
    selected_option = answer['option']

    if selected_option == "Volver al menú":
        mostrar_menu(user, session)
    if selected_option == "Continuar con otra búsqueda":
        buscar_perfiles_por_nombre(user, session)
    elif selected_option == menu_a:            
        trackist_musician(perfil_select, user) if perfil_select.type == "musician" else playlist_album(perfil_select, user) 
    else:
        print("Opción inválida. Intente nuevamente.")





def trackist_musician(perfil_select, user):
    perfil_id = perfil_select.id

    try:
        with open('albums.txt', 'r') as f:
            albums_data = json.load(f)
    except FileNotFoundError:
        print("El archivo albums.txt no existe.")
        return  # Salir de la función si no se puede cargar el archivo
    
    # Buscar todos los álbumes del artista específico
    # print(f"Álbum del artista con ID {perfil_id}")
    # print("Lista de álbumes:")
    albums_del_artista = []
    albums_choices = []  # Lista para almacenar las opciones de álbumes para Inquirer
    for album_data in albums_data:
        if album_data['artist'] == perfil_id:
            album_del_artista = Albums(**album_data)
            albums_del_artista.append(album_del_artista)
            albums_choices.append((album_del_artista.name, album_del_artista))  # Agregar opción de álbum a la lista

    if not albums_del_artista:
        print(f"No se encontró ningún álbum para el artista {perfil_select.name}")

    print("Submenu musician 🎸" )

    while True:
        album_questions = [
            inquirer.List('option',
                          message="Seleccione un álbum:",
                          choices=albums_choices + [("Volver al menú anterior", None)],  # Agregar la opción para volver al menú principal
                          ),
        ]
        album_answers = inquirer.prompt(album_questions)
        selected_album = album_answers['option']

        if selected_album is None:  # Si el usuario elige volver al menú principal
            submenulist(perfil_select, user)
            # continue
            


        # Crear lista de opciones de canciones
        enum_tracklist = enumerate(selected_album.tracklist, start=1)

        music_list = {}

        # Iterar sobre cada pista en el álbum
        for i, track in enum_tracklist:
            music_list[track.name] = track.link

        # Convertir el diccionario a formato JSON
        json_data  = json.dumps(music_list, indent=4)

        # Ahora, asegurémonos de que music_list sea un diccionario
        music_list = json.loads(json_data)

        # print(json_data)


        # A partir de aquí, puedes usar music_list como un diccionario
        reproducir_listado(music_list, perfil_select, user)





player = MediaPlayer()

def reproducir_listado(music_list, perfil_select, user):
    questions = [
        inquirer.List(
            "selected_option",
            message="Seleccione una opción:",
            choices=list(music_list.keys()) + ["Detener"] + ["Regresar"],
        )
    ]

    while True:
        answers = inquirer.prompt(questions)
        selected_option = answers["selected_option"]

        if selected_option in music_list:
            print(f"Reproduciendo {selected_option}...")
            player.play(music_list[selected_option])
        elif selected_option == "Detener":
            player.stop()
             
        elif selected_option == "Regresar":
            player.stop()
            playlist_album(perfil_select, user)
            return  # Regresa al código que llamó a esta función
        else:
            print("Opción inválida. Intente nuevamente.")
        


#modificando aqui listener
def playlist_album(perfil_select, user):
    perfil_id = perfil_select.id

    # Cargar los datos de las playlists
    try:
        with open('playlist.txt', 'r') as f:
            playlist_data = json.load(f)
    except FileNotFoundError:
        print("El archivo playlist.txt no existe.")
        return

    # Cargar los datos de los álbumes
    try:
        with open('albums.txt', 'r') as f:
            albums_data = json.load(f)
    except FileNotFoundError:
        print("El archivo albums.txt no existe.")
        return

    # Buscar las playlists del usuario
    playlist_del_user = [playlis for playlis in playlist_data if playlis['creator'] == perfil_id]
    if not playlist_del_user:
        print(f"No se encontró ninguna playlist para el listener con ID {perfil_id}")
        return
    
    # Mostrar las playlists y seleccionar una
    playlist_choices = [(playlis['name'], playlis) for playlis in playlist_del_user]

    # Agregar la opción para regresar al submenú
    playlist_choices.append(("Regresar al submenú", None))
    
    selected_playlist = inquirer.prompt([
        inquirer.List('option', message="Seleccione una playlist", choices=playlist_choices)
    ])['option']

    # Si el usuario selecciona "Regresar al submenú", termina la función
    if selected_playlist is None:
        submenulist(perfil_select, user)
        
    

    # Buscar las canciones en los álbumes usando los IDs de las canciones de la playlist seleccionada
    canciones_encontradas = []
    for track_id in selected_playlist['tracks']:
        for album in albums_data:
            for track in album['tracklist']:
                if track['id'] == track_id:
                    canciones_encontradas.append(track)

    # Imprimir el listado de las canciones
    music_list = {}
    for i, cancion in enumerate(canciones_encontradas, start=1):
        music_list[cancion['name']] = cancion['link']
    # print(music_list)
    
    # # Crear una instancia de MediaPlayer
    # player = MediaPlayer()
    
    reproducir_listado(music_list, perfil_select, user)





def cerrar_sesion(session):
    print("¿Quiere cerrar la sesión? ")

    questions = [
        inquirer.List('confirm',
                      message="Seleccione una opción",
                      choices=['Sí', 'No'],
                      ),
    ]
    answer = inquirer.prompt(questions)
    confirmation = answer['confirm']

    if confirmation == 'Sí':
        if session:
            session.end_session()
            session = None
        # Aquí iría la lógica para eliminar la cuenta
        print("sesion cerrada correctamente.")
        mostrar_menu()
    else:
        print("Operación cancelada. Su cuenta no se cerro.")
   
    # Mostrar los perfiles encontrados


def buscar_usuario_por_id(user_id):
    try:
        with open('users.txt', 'r') as file:
            users_data = json.load(file)
            for user_data in users_data:
                if user_data['id'] == user_id:
                    return user_data    
    except FileNotFoundError:
        print("El archivo users.txt no existe.")
    except Exception as e:
        print(f"No se pudo buscar el usuario: {e}")
    return None


def actualizar_informacion_personal(user=None):
    if not user:
        print("Debe iniciar sesión para actualizar la información personal.")
        return
    
    user_id = user.id
    user_data = buscar_usuario_por_id(user_id)
    if not user_data:
        print("No se encontró información del usuario.")
        return

    # print(f"Usuario encontrado: {user_data}")

    # Solicitar al usuario que ingrese la nueva información personal
    print(user_data['name'])
    new_name = input(f"Ingrese el nuevo nombre: ")
    print(user_data['email'])
    new_email = input(f"Ingrese el nuevo correo electrónico: ")
    print(user_data['username'])
    new_username = input(f"Ingrese el nuevo nombre de usuario: ")
    new_password = getpass.getpass("Ingrese su nueva contraseña: ")
    print(user_data['type'])

    type = [
        inquirer.List('size',
                        message="Seleccione el tipo de usuario: ",
                        choices=['musician','listener']
                        )                
    ]
    new_type_select = inquirer.prompt(type)['size']

    # Actualizar la información personal en los datos del usuario
    user_data['name'] = new_name if new_name else user_data['name']
    user_data['email'] = new_email if new_email else user_data['email']
    user_data['username'] = new_username if new_username else user_data['username']
    user_data['password'] = new_password if new_password else user_data['password']
    user_data['type'] = new_type_select if new_type_select else user_data['type']

    # Actualizar los datos del usuario en el archivo users.txt
    try:
        with open('users.txt', 'r') as file:
            users_data = json.load(file)

        for i, data in enumerate(users_data):
            if data['id'] == user_id:
                users_data[i] = user_data

        with open('users.txt', 'w') as file:
            json.dump(users_data, file, indent=4)

        print("Información actualizada correctamente.")
    except Exception as e:
        print(f"No se pudo actualizar la información: {e}")

    mostrar_menu(user)


    

def borrar_cuenta(user=None, session=None):
    def eliminar_usuario(user_id):
        try:
            # Cargar los datos actuales del archivo
            with open('users.txt', 'r') as file:
                users = json.load(file)

            # Eliminar el usuario del listado
            users = [user_data for user_data in users if user_data.get('id') != user_id]

            # Escribir la lista actualizada de usuarios en el archivo
            with open('users.txt', 'w') as file:
                json.dump(users, file, indent=4)

            print("Usuario eliminado correctamente.")
        except Exception as e:
            print(f"No se pudo eliminar el usuario: {e}")

    if session is None:
        print("Debe iniciar sesión para poder eliminar su cuenta.")
        return

    if user is None:
        print("Debe proporcionar información de usuario para eliminar la cuenta.")
        return

    if isinstance(user, User):
        user_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'username': user.username,
            'type': user.type,
            'password': user.password
        }
    else:
        user_data = user

    # Obtener el token de la sesión o proporcionar uno si no está disponible
    token = getattr(session, 'token', None) or 'default_token_value'

    # Crear una nueva instancia de Session con los datos del usuario y el token
    session = Session(user_data['id'], user_data, token)

    print("¿Está seguro de que desea eliminar su cuenta?")

    questions = [
        inquirer.List('confirm',
                      message="Seleccione una opción:",
                      choices=['Sí', 'No'],
                      ),
    ]
    answer = inquirer.prompt(questions)
    confirmation = answer['confirm']

    if confirmation == 'Sí':
        if session.id:  # Verifica si el atributo id del usuario de la sesión está presente
            eliminar_usuario(session.id)  # Eliminar el usuario usando su id
            session.end_session()  # Cerrar la sesión antes de volver al menú principal
        else:
            print("No se encontró información del usuario.")
    else:
        print("Operación cancelada. Su cuenta no se ha eliminado.")





# Bucle principal
if __name__ == "__main__":
    cargar_datos()
    guardar_datos()
    cargar_album_api()
    guardar_albums()
    mostrar_menu(user=None)

    
