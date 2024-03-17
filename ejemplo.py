import uuid

def generar_id_album():
    # Genera un UUID
    unique_id = str(uuid.uuid4())

    # Formatea el UUID como b48bf9e9-cff4-4313-a61f-4d39b9a40ce2
    formatted_id = f"{unique_id[0:8]}-{unique_id[9:13]}-{unique_id[14:18]}-{unique_id[19:23]}-{unique_id[24:]}"

    return formatted_id

# Llama a la función para generar un ID único con el formato especificado
id_album_resultado = generar_id_album()
print(f"ID único con formato: {id_album_resultado}")
