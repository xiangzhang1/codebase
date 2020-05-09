import subprocess
import ase, ase.io
from toolkit.utils import POTCAR_PATH, LIB_PATH, periodic_table_lookup, template

# ----------------------------------------------------------------------------------------------------------------------

def to_vasp(d, struct):
    """Writes INCAR, POSCAR4, KPOINTS, POTCAR. Copies CHGCAR/WAVECAR.

    Parameters
    ----------
    d : D                               # 材料相关，求值模式，简化近似，辅助行为
        hidden: {'hidden'}              # 不写入 INCAR
        kpoints: ['template', ...]      # KPOINTS 模板
        psi0|rho0|rho = 0|path          # 迭代初始值
    struct : Struct
    """
    with open("INCAR", "w") as file:
        for k, v in d.items():
            if k not in d['hidden']:
                file.write("{k} = {v}\n")
    #
    atoms = ase.Atoms(symbols=struct.XS.S, positions=struct.XS[['X', 'Y', 'Z']], cell=struct.A)
    ase.io.write("POSCAR", images=atoms, format="vasp")
    #
    template(i = f"{LIB_PATH}/KPOINTS.{d['kpoints'][0]}", o = "KPOINTS", d = d)
    #
    for symbol in struct.stoichiometry:
        potcar = POTCAR_PATH + periodic_table_lookup(symbol, "pot") + "/POTCAR"
        subprocess.run(f"cat {potcar} >> POTCAR", shell=True)
    #
    for path in [d[k] for k in ['rho', 'rho0', 'phi0'] if k in d]:
        subprocess.run(f"rsync -a -h --info=progress2 {path} .", shell=True)

# ----------------------------------------------------------------------------------------------------------------------

def to_slurm(d):
    """
    Parameters
    ----------
    d: D
        software: 'vasp'
        cluster: 'nersc'
    """
    template(i = f"{LIB_PATH}/submit.{d['software']}.{d['cluster']}", o = "submit", d = d)
    template(i = f"{LIB_PATH}/job.{d['software']}.{d['cluster']}", o = "job", d = d)

def submit():
    subprocess.run("bash submit", shell=True)

def is_complete(d):
    template(i=f"{LIB_PATH}/is_complete.{d['cluster']}", o="is_complete", d = d)
    return eval(subprocess.check_output("bash is_complete", shell=True))

def retrieve(d):
    template(i=f"{LIB_PATH}/retrieve.{d['cluster']}", o="retrieve", d = d)
    subprocess.run("bash retrieve", shell=True)

class Pending(Exception):
    pass

def try_retrieve(d):
    """For recursion.

    Raises
    ------
    Pending
        If `not is_complete()`.
    """
    if is_complete(d):
        retrieve(d)
    else:
        raise Pending