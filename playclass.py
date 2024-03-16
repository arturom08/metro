import subprocess

class MediaPlayer:
    # Definir vlc_path como un atributo de clase
    vlc_path = "C:/Program Files/VideoLAN/VLC/vlc.exe"

    def __init__(self):
        self.player_process = None

    def play(self, url):
        command = [self.vlc_path, "--intf", "dummy", url]

        # Si hay un proceso de reproductor en ejecución, terminarlo
        if self.player_process is not None:
            self.player_process.terminate()

        # Iniciar un nuevo proceso de reproductor
        self.player_process = subprocess.Popen(command)

    def stop(self):
        if self.player_process is not None:
            self.player_process.terminate()
