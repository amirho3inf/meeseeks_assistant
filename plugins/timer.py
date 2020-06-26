from assistant import assistant, filters, utils
from threading import Thread, Event
from word2number import w2n
import time


"""
Command:                      Description:

time it for two minutes       set a timer for 2 minutes and stops command mode
timer for fifty seconds       set a timer for 50 minutes and stops command mode
stop timer                    stops the timer in progress
"""

TIME_DURATION_UNITS = (
    ('hour', 60*60),
    ('minute', 60),
    ('second', 1)
)

TIMER_EVENT = Event()


def human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'.format(
                amount, unit, "" if amount == 1 else "s"))
    return ' and '.join(parts)


class Timer(Thread):
    def __init__(self, seconds: int, mute: bool = False, *args, **kwargs):
        super(Timer, self).__init__(*args, **kwargs)
        self.seconds = seconds
        self.mute = mute

        # Start thread
        self.start()

    def run(self):
        TIMER_EVENT.set()
        human_time = human_time_duration(self.seconds)
        time.sleep(0.5)
        utils.tts(f'timer for {human_time}' +
                  ('without sound' if self.mute is True else ''))
        time.sleep(0.5)
        utils.tts('start')
        self._time_it_and_block()

        if TIMER_EVENT.is_set():
            utils.play('ding.wav')
            TIMER_EVENT.clear()

    def _time_it_and_block(self):
        start_time = time.time()

        while (time.time() - start_time < self.seconds) and TIMER_EVENT.is_set():
            if self.mute is True:
                time.sleep(1)
            else:
                utils.play("kitchen timer sound.wav")


@assistant.register_handler(
    filters.contains('time'),
    filters.contains('for'),
    filters.regexp(r'.*(second|minute|hour).*'))
def timer(cmd, regexp):
    try:
        n = w2n.word_to_num(cmd)
    except ValueError:
        # No valid numeric words found!
        return False

    # The unit matched by regex pattern filter
    unit = regexp.groups()[0]

    secs = 0
    for u, t in TIME_DURATION_UNITS:
        if u == unit:
            secs = n * t

    # without kitchen timer sound
    without_timer_sound = ("without" in cmd or "mute" in cmd)

    if TIMER_EVENT.is_set():
        utils.tts('currently a timer is in progress')
        utils.tts('you can stop that by saying')
        utils.tts('stop timer')
        return False

    utils.play('oow okay.wav')
    Timer(seconds=secs, mute=without_timer_sound)

    return True


@assistant.register_handler(
    filters.contains('stop'),
    filters.contains('time'),
    lambda cmd: TIMER_EVENT.is_set())
def stop_timer(cmd):
    TIMER_EVENT.clear()
    utils.play("that's okay.wav")
    return False
