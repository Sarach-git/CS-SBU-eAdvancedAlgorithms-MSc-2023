import pathlib

import pandas as pd

from diet import consts
from diet_lp import settings

__foods = None
__foods_mapping = None


def get_foods():
    global __foods
    if __foods is None:
        current_directory = pathlib.Path(__file__).resolve().parent
        __foods = pd.read_csv(current_directory / settings.FOOD_CSV)

    return __foods


def get_foods_mapping():
    global __foods_mapping
    if __foods_mapping is None:
        foods = get_foods()
        __foods_mapping = {}
        for _, row in foods.iterrows():
            __foods_mapping[row[consts.COLUMN_FDC_ID]] = row[consts.COLUMN_DESCRIPTION]

    return __foods_mapping
