from meeseeks import Meeseeks
import config

assistant = Meeseeks(
    vosk_model=config.VOSK_MODEL,
    hotword_models=config.HOTWORD_MODELS,
    sensitivity=config.SENSITIVITY,
    command_mode_time=config.COMMAND_MODE_DURATION
)
