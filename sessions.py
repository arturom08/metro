import json
import uuid
from user import User 

class Session:
    def __init__(self, id, user, token=None):
        self.id = id
        self.user = user
        self.token = token

    def is_valid(self):
        # Lógica para verificar si la sesión es válida (por ejemplo, verificar la vigencia del token)
        pass
    
    @staticmethod
    def generar_token():
        # Utiliza la función uuid para generar un token único
        return str(uuid.uuid4())


    @staticmethod
    def iniciar_sesion(email, password):
        try:
            with open('users.txt', 'r') as f:
                users = json.load(f)
                for user_data in users:
                    if user_data['email'] == email and user_data['password'] == password:
                        user = User(**user_data)  # Crea una instancia de User con los datos del usuario
                        # Suponiendo que el token se genera de alguna manera
                        token = Session.generar_token()  # Genera un token único
                        return user, token  # Devuelve el usuario y el token si las credenciales son válidas
                print("Correo electrónico o contraseña incorrectos.")
                return None, None
        except Exception as e:
            print(f"No se pudo iniciar sesión: {e}")
            return None, None


    def end_session(self):
        # Método para finalizar la sesión
        self.user = None  # Elimina el usuario de la sesión
        self.token = None  # Elimina el token de la sesión
        print("Sesión finalizada correctamente.")

# Funciones para iniciar, verificar y finalizar sesiones de usuario

# main.py (archivo principal del programa)
# Lógica principal del programa, incluyendo la interacción con el usuario y el manejo de solicitudes
# Puedes importar las clases y funciones relevantes de users.py y sessions.py según sea necesario aquí

if __name__ == "__main__":
    # Lógica de inicio del programa
    pass
