#/usr/bin/env python3


def try_int(arg, default):
    try:
        arg = int(arg)
    except TypeError:
        arg = default
    except ValueError:
        arg = default
    return arg
