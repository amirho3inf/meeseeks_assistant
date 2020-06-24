import subprocess
import config
from playsound import playsound


def tts(text):
    cmd = ['flite', '-voice', config.FLITEVOX_FILE, '-t', text]
    subprocess.run(cmd)


def play(audio):
    file_path = f"{config.AUDIOS_DIR}/{audio}"
    playsound(file_path)
