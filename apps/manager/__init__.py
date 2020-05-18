import os
from apps.manager.json import load, dump

PROJECTS = os.path.dirname(__file__)


def load_manager():
    return load(f"{PROJECTS}/manager.json")


def dump_manager(manager):
    dump(manager, f"{PROJECTS}/manager.json")