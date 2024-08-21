# __init__.py

from _msp3520 import init as _init, show as _show

def init():
    return _init()

def show(text, x, y):
    return _show(text, x, y)
