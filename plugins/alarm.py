from assistant import assistant, filters


@assistant.register_handler(filters.contains("set alarm"))
def handle(cmd):
    print(cmd)


def handle2(cmd):
    print(cmd)


assistant.add_handler(handle2, filters.contains("delete alarm"))
