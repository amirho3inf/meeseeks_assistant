import re


def regexp(pattern):
    """
    Regexp filter for commands
    This filter gives 'regexp' keyword argument to the handler
    """
    patt = re.compile(pattern)

    def inner(cmd):
        r = patt.match(cmd)
        if r is None:
            return False
        return {"regexp": r}
    return inner


def contains(text):
    """
    Contains filter for commands
    This filter doesn't give any argument to the handler
    """
    def inner(cmd):
        return (text in cmd)
    return inner


def equals(text):
    """
    Equals filter for commands
    This filter doesn't give any argument to the handler
    """
    def inner(cmd):
        return (text == cmd)
    return inner
