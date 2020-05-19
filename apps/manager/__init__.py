import os
from apps.io.json import load, dump

SAVEFILE = os.path.join(os.path.dirname(__file__), 'manager.json')


def load_manager():
    return load(SAVEFILE)


def dump_manager(manager):
    dump(manager, SAVEFILE)