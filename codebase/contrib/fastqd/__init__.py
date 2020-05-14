from shutil import copy
from codebase.toolkit.common import dict2str, template
from codebase.toolkit.io.vasp import struct2poscar

TEMPLATES = os.path.join(os.path.realpath(__file__), 'templates')


def expand(d, struct):
    d['stoichiometry'] = dict2str(struct.stoichiometry)
    d.exec_file(f"{DIR}/rules.py")


def to_vasp(d, struct):
    template(
        i=f"{TEMPLATES}/INCAR",
        o="INCAR",
        d=d
    )

    struct2poscar(struct, "POSCAR")

    copy(f"{TEMPLATES}/KPOINTS", "KPOINTS")

    copy(f"{TEMPLATES}/POTCAR", "POTCAR")

def to_slurm(d, struct):
    """
    Parameters
    ----------
    d : D
        software: 'templates'
        cluster: 'knl'
        queue: 'regular'
        nnode: 4
    struct : Struct
    """
    template(i = f"{TEMPLATES}/templates/submit.{d['software']}.{d['cluster']}", o ="submit", d = d)
    template(i = f"{TEMPLATES}/templates/job.{d['software']}.{d['cluster']}", o ="job", d = d)
