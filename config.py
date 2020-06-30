# path of vosk api model
# download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md
# unpack as vosk-api in models directory
VOSK_MODEL = "assets/models/vosk-api"

# list of snowboy models
# make these models here: https://snowboy.kitt.ai/dashboard
HOTWORD_MODELS = [
    "assets/models/meeseeks.pmdl",
]

# sensitivity of snowboy hotword detector
SENSITIVITY = 0.4

# command mode duration in seconds
# command mode is the state after waking up that the assistant waits to get the commands
COMMAND_MODE_DURATION = 30

# path of flite voice file
# download from http://festvox.org/flite/packed/flite-2.1/voices/
FLITEVOX_FILE = "assets/models/cmu_us_bdl.flitevox"

# path of audios directory
AUDIOS_DIR = "assets/audios"

# path of plugins directory
PLUGINS_DIR = "plugins"

# list of enabled plugins
# priority order is important
PLUGINS = [
    "main",
    "timer",
    "time",
]
