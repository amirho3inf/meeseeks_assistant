"""
Command:                Description:

stop this               stops command mode
go to sleep             stops command mode
"""

from assistant import assistant, filters, utils


@assistant.register_handler(filters.equals('stop this'))
@assistant.register_handler(filters.contains('go to sleep'))
def stop_cmd_mode(cmd):
    utils.play('oow okay.wav')
    assistant.stop_command_check()
    return True
