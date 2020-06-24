from assets.snowboy.snowboydecoder import HotwordDetector
from vosk import Model, KaldiRecognizer
import pyaudio
import time
import signal
import json


class Meeseeks(object):
    def __init__(self,
                 vosk_model: str,
                 hotword_models: list,
                 command_mode_time: int = 10,
                 sensitivity: float = 0.5):
        self.interrupted = False
        self.hotword_detector = HotwordDetector(
            hotword_models, sensitivity=sensitivity)
        self.hotword_said = False
        self.vosk_model = Model(vosk_model)
        self.command_mode_time = command_mode_time
        signal.signal(signal.SIGINT, self.on_signal)
        self.handlers = []

    def on_signal(self, signal, frame):
        self.interrupted = True

    def hotword_interrupt_check(self):
        return self.hotword_said or self.interrupted

    def on_hotword(self):
        self.hotword_said = True

    def hotword_check(self):
        self.hotword_said = False
        self.hotword_detector.start(detected_callback=self.on_hotword,
                                    interrupt_check=self.hotword_interrupt_check,
                                    sleep_time=0.03)
        self.hotword_detector.terminate()
        return True

    def _make_filtered_handler(self, func, filters):
        def inner(cmd):
            kwargs = {}
            for f in filters:
                ret = f(cmd)
                if isinstance(ret, dict):
                    kwargs.update(ret)
                if ret is False:
                    return False
            func(cmd, **kwargs)
        return inner

    def add_handler(self, func, *filters):
        if callable(func) is False:
            raise Exception("Arg must be callable")
        handler = self._make_filtered_handler(func, filters)
        self.handlers.append(handler)

    def register_handler(self, *filters):
        def deco(func):
            handler = self._make_filtered_handler(func, filters)
            self.handlers.append(handler)
            return func
        return deco

    def handle_command(self, cmd):
        for handler in self.handlers:
            if handler(cmd) is True:
                return

    def command_interrupt_check(self):
        its_over = time.time() - self._cmd_start_t > self.command_mode_time
        return its_over or self.interrupted

    def command_check(self):
        self._cmd_start_t = time.time()
        speech_recognizer = KaldiRecognizer(self.vosk_model, 16000)
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1,
                        rate=16000, input=True, frames_per_buffer=8000)
        stream.start_stream()
        while not self.command_interrupt_check():
            data = stream.read(4000)
            if len(data) == 0:
                break
            if speech_recognizer.AcceptWaveform(data):
                jdata = json.loads(speech_recognizer.Result())
                cmd = jdata.get("text")
                if cmd:
                    self.handle_command(cmd)
        stream.stop_stream()

    def run(self):
        while self.hotword_check() and not self.interrupted:
            self.command_check()
