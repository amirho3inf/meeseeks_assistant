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

        self._hotword_detector = HotwordDetector(
            hotword_models, sensitivity=sensitivity)
        self._vosk_model = Model(vosk_model)
        self._cmd_start_t = 0
        self._cmd_start_f = lambda: None
        self._cmd_stop_f = lambda: None

        self.handlers = []
        self.command_mode_time = command_mode_time
        self.interrupted = False
        self.hotword_said = False

        signal.signal(signal.SIGINT, self._on_signal)

    def _on_signal(self, signal, frame):
        self.interrupted = True

    def _hotword_interrupt_check(self):
        return self.hotword_said or self.interrupted

    def _on_hotword(self):
        self.hotword_said = True

    def _hotword_check(self):
        print('+ Switch to hotword mode')
        self.hotword_said = False
        self._hotword_detector.start(detected_callback=self._on_hotword,
                                     interrupt_check=self._hotword_interrupt_check,
                                     sleep_time=0.03)
        self._hotword_detector.terminate()
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
            return func(cmd, **kwargs)
        return inner

    def _handle_command(self, cmd):
        for handler in self.handlers:
            if handler(cmd) is True:
                self.stop_command_check()
                return

    def _command_interrupt_check(self):
        its_over = time.time() - self._cmd_start_t > self.command_mode_time
        return its_over or self.interrupted

    def _command_check(self):
        print('+ Switch to command mode')
        self._cmd_start_t = time.time()
        speech_recognizer = KaldiRecognizer(self._vosk_model, 16000)
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1,
                        rate=16000, input=True, frames_per_buffer=8000)
        stream.start_stream()
        self._cmd_start_f()
        while not self._command_interrupt_check():
            data = stream.read(4000)
            if len(data) == 0:
                break
            if speech_recognizer.AcceptWaveform(data):
                jdata = json.loads(speech_recognizer.Result())
                cmd = jdata.get("text")
                print("CMD:", cmd, end=f"\n-----{'-'*len(cmd)}\n")
                if cmd:
                    self._handle_command(cmd)
        stream.stop_stream()
        self._cmd_stop_f()

    def stop_command_check(self):
        self._cmd_start_t = 0

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

    def on_command_mode_start(self, func):
        if callable(func) is False:
            raise Exception("Arg must be callable")
        self._cmd_start_f = func
        return func

    def on_command_mode_stop(self, func):
        if callable(func) is False:
            raise Exception("Arg must be callable")
        self._cmd_stop_f = func
        return func

    def run(self):
        while self._hotword_check() and not self.interrupted:
            self._command_check()
