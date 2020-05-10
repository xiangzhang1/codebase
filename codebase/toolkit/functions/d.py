def exec_file(path, d):
    # 文件用 # 分块
    for i in range(3):
        with open(path, "r") as file:
            for block in file.read().split('#'):
                try:
                    d.exec_('#' + block)
                except:
                    if i == 2:
                        raise


def exec_shorthand(text, d):
    # exec_shorthand(d, "insulator, qd, spin=fm")
    for _ in text.split(','):
        _ = _.strip()
        if '=' not in _:        # insulator
            d[_] = None
        else:                   # kpoints=[1,1] or spin=fm
            l, r = _.split('=')
            l, r = l.strip(), r.strip()
            try:                # kpoints=[1,1]
                d[l] = eval(r)
            except NameError:   # spin=fm
                d[l] = r