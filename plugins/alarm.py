from assistant import assistant
from filters import contains


@assistant.register_handler(contains("set alarm"))
def handle(cmd):
    print(cmd)


def handle2(cmd):
    print(cmd)


assistant.add_handler(handle2, contains("delete alarm"))
