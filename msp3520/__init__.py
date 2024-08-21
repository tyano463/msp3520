# __init__.py

from .msp3520 import init as _init, show as _show

def init():
    _init()

def show(text, x, y):
    _show(text.encode('utf-8'), x, y)

