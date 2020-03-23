import atomics
import conveniences

class D(atomics.D):
    """d = D('vasp, spin=fm').expand()"""

    def __init__(self):
        super().__init__()
        self.