import os
import pandas as pd
from apps.io.json import load, dump


SAVEFILE = os.path.join(os.path.dirname(__file__), 'relations.json')

sample_relations = {
    'opt->opt': pd.DataFrame(columns=['prev', 'next'], dtype=str),
    'bad_fulfillment': pd.DataFrame(columns=['bad_fulfillment', 'try_again'], dtype=str),
}


def load_relations():
    return load(SAVEFILE)


def dump_relations(relations):
    dump(relations, SAVEFILE)