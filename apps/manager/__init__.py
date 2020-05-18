import os
from apps.manager.json import load, dump

SAVE_FOLDER = os.path.dirname(__file__)


def load_manager():
    return load(f"{SAVE_FOLDER}/manager.json")


def dump_manager(manager):
    dump(manager, f"{SAVE_FOLDER}/manager.json")