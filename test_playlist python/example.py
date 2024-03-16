import inquirer
from playclass import MediaPlayer

# Diccionario de URLs
urls = {
    "musica 1": "https://soundcloud.com/itsproppa/proppagfys?in=luk_music/sets/ibiza-techno-house-2024-summer-mix&utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing",
    "musica 2": "https://soundcloud.com/nacho-p-476254323/baby-one-more-time-feat-jack-black-from-kung-fu-panda-4soundtrack-version",
    "musica 3": "https://soundcloud.com/vgmplanet/sets/secret-of-mana-ost",
    # Agrega más URLs aquí
}

# Ruta al ejecutable VLC


# Crear una instancia de MediaPlayer
player = MediaPlayer()

questions = [
    inquirer.List(
        "selected_option",
        message="Seleccione una opción:",
        choices=list(urls.keys()) + ["Salir"],
    )
]

while True:
    answers = inquirer.prompt(questions)
    selected_option = answers["selected_option"]

    if selected_option in urls:
        print(f"Reproduciendo {selected_option}...")
        player.play(urls[selected_option])
    elif selected_option == "Salir":
        player.stop()        
    else:
        print("Opción inválida. Intente nuevamente.")
