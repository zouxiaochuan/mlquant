import logging
import sys

console = logging.getLogger("console")

if not console.hasHandlers():
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    console.addHandler(ch)
    pass

def setLevel(level):
    console.setLevel(level)

