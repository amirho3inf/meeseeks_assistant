"""
Command:                Description:

what time is it         tells the local time
"""

from assistant import assistant, filters, utils
import time


@assistant.register_handler(
    filters.contains('what'),
    filters.contains('time')
)
def what_time(cmd):
    now = time.strftime("%I:%M")
    utils.tts(now)
    return True
