from assistant import assistant, utils
import config
import importlib
import traceback
import random


for plug in config.PLUGINS:
    try:
        print(f"Loading {plug}")
        importlib.import_module(f'{config.PLUGINS_DIR}.{plug}')
    except Exception:
        traceback.print_exc()


@assistant.on_command_mode_start
def on_cmd_start():
    aus = ["i'm mr meeseeks 2.wav",
           "i'm mr meeseeks.wav"]
    au = random.choice(aus)
    utils.play(au)


@assistant.on_command_mode_stop
def on_cmd_stop():
    utils.play('box sound.wav')


assistant.run()
