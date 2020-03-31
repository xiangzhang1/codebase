from toolbox.barebones.functions import is_complete, retrieve

class Pending(Exception):
    pass

def try_retrieve(d):
    if is_complete(d):
        retrieve(d)
    else:
        raise Pending