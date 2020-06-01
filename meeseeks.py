from assets.snowboy.snowboydecoder import HotwordDetector
from vosk import Model, KaldiRecognizer
import pyaudio
import time
import signal


class Meeseeks(object):
    def __init__(self,
                 vosk_model: str,
                 hotword_models: list,
                 command_mode_time: int = 30,
                 sensitivity: float = 0.5):
        self.interrupted = False
        self.hotword_detector = HotwordDetector(
            hotword_models, sensitivity=sensitivity)
        self.hotword_said = False
        vosk_model = Model(vosk_model)
        self.speech_recognizer = KaldiRecognizer(vosk_model, 16000)
        self.command_mode_time = command_mode_time
        signal.signal(signal.SIGINT, self.on_signal)

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

    def command_interrupt_check(self):
        return time.time() - self._cmd_start_t > self.command_mode_time

    def command_check(self):
        self._cmd_start_t = time.time()
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1,
                        rate=16000, input=True, frames_per_buffer=8000)
        stream.start_stream()
        while not self.command_interrupt_check():
            data = stream.read(4000)
            if len(data) == 0:
                break
            if self.speech_recognizer.AcceptWaveform(data):
                res = self.speech_recognizer.Result()
                print(res)
        res = self.speech_recognizer.PartialResult()
        print(res)
        stream.stop_stream()

    def run(self):
        while self.hotword_check() and not self.interrupted:
            self.command_check()


meeseeks = Meeseeks(vosk_model="assets/models/vosk-api",
                    hotword_models=["assets/models/meeseeks.pmdl"])
meeseeks.run()
