import subprocess
import config
from playsound import playsound


def tts(text):
    """
    Text-to-speech using flite
    """
    cmd = ['flite', '-voice', config.FLITEVOX_FILE,
           '-t', text, '--setf', 'duration_stretch=1.3']
    subprocess.run(cmd)


def play(audio):
    """
    Play a audio from config.AUDIOS_DIR
    """
    file_path = f"{config.AUDIOS_DIR}/{audio}"
    playsound(file_path)
