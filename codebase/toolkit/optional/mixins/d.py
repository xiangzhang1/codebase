class DMixin(object):
    """
    Adds behaviour (and nothing else) to D and Struct via `Mixin<https://stackoverflow.com/q/533631/6417519>`_'s.

    Funnily enough, the `objects` module imports the `optional` module.
    """

    def exec_file(self, filename):
        with open(filename) as rules:
            exec(rules.read(), globals(), self)

    def exec_shorthand(text, self):
        # exec_shorthand(d, "insulator, qd, spin=fm")
        for _ in text.split(','):
            _ = _.strip()
            if '=' not in _:        # insulator
                self[_] = None
            else:                   # kpoints=[1,1] or spin=fm
                l, r = _.split('=')
                l, r = l.strip(), r.strip()
                try:                # kpoints=[1,1]
                    self[l] = eval(r)
                except NameError:   # spin=fm
                    self[l] = r