import re


def regexp(pattern):
    patt = re.compile(pattern)

    def inner(cmd):
        r = patt.match(cmd)
        if r is None:
            return False
        return {"regexp": r}
    return inner


def contains(text):
    def inner(cmd):
        return (text in cmd)
    return inner


def equals(text):
    def inner(cmd):
        return (text == cmd)
    return inner
