import pathlib
import re
from functools import reduce

import typing

import pandas as pd

from diet import consts


def preprocess(foods: pd.DataFrame, food_nutrients: pd.DataFrame) -> pd.DataFrame:
    _filter(foods)

    foods = foods.drop(['data_type', 'publication_date'], axis=1)

    _add_columns(foods, food_nutrients)

    foods = foods.dropna(how='any')

    foods = foods.reset_index(drop=True)

    return foods


def _filter(foods: pd.DataFrame):
    wanted_category_ids = list(map(
        consts.category_id_mapper,
        reduce(
            lambda x, y: x.union(y),
            [
                consts.MEAL_FOOD_CATEGORY_MAPPING[consts.MEAL_BREAKFAST],
                consts.MEAL_FOOD_CATEGORY_MAPPING[consts.MEAL_MORNING_SNACK],
                consts.MEAL_FOOD_CATEGORY_MAPPING[consts.MEAL_LUNCH],
                consts.MEAL_FOOD_CATEGORY_MAPPING[consts.MEAL_AFTERNOON_SNACK],
                consts.MEAL_FOOD_CATEGORY_MAPPING[consts.MEAL_DINNER],
            ],
            set(),
        )
    ))

    for index, row in foods.iterrows():
        # 1
        if row[consts.COLUMN_FOOD_CATEGORY_ID] not in wanted_category_ids:
            foods.drop(index, inplace=True)
            continue

        # 2
        if _contains_any_of_words(row[consts.COLUMN_DESCRIPTION], ["raw", "unprepared"]):
            foods.drop(index, inplace=True)
            continue

        # 3
        if (
                row[consts.COLUMN_FOOD_CATEGORY_ID] ==
                consts.category_id_mapper(consts.FOOD_CATEGORY_SOUPS_SAUCES_AND_GRAVIES)
        ):
            if _contains_any_of_words(row[consts.COLUMN_DESCRIPTION], ["sauce"]):
                foods.drop(index, inplace=True)
                continue

        # 4
        if _contains_any_of_words(
                row[consts.COLUMN_DESCRIPTION],
                [
                    "quail", "pheasant", "dove", "squab", "goose", "duck", "guinea hen", "grouse", "emu", "ostrich",
                    "ham", "pork", "bacon", "alcohol", "alcoholic", "beer", "wine", "whiskey", "gin", "rum",
                    "vodka", "liquor",
                ],
        ):
            foods.drop(index, inplace=True)
            continue

        # 5
        if (
                row[consts.COLUMN_FOOD_CATEGORY_ID] ==
                consts.category_id_mapper(consts.FOOD_CATEGORY_FINFISH_AND_SHELLFISH_PRODUCTS)
        ):
            if not _contains_any_of_words(row[consts.COLUMN_DESCRIPTION], ["salmon", "tuna", "shrimp"]):
                foods.drop(index, inplace=True)
                continue

        # 6
        if (
                row[consts.COLUMN_FOOD_CATEGORY_ID] ==
                consts.category_id_mapper(consts.FOOD_CATEGORY_LAMB_VEAL_AND_GAME_PRODUCTS)
        ):
            if _contains_any_of_words(row[consts.COLUMN_DESCRIPTION], ["game"]):
                foods.drop(index, inplace=True)
                continue

        # 7
        if (
                row[consts.COLUMN_FOOD_CATEGORY_ID] ==
                consts.category_id_mapper(consts.FOOD_CATEGORY_BAKED_PRODUCTS)
        ):
            if not _contains_any_of_words(row[consts.COLUMN_DESCRIPTION], ["bread"]):
                foods.drop(index, inplace=True)
                continue

        # 8
        if (
                row[consts.COLUMN_FOOD_CATEGORY_ID] ==
                consts.category_id_mapper(consts.FOOD_CATEGORY_CEREAL_GRAINS_AND_PASTA)
        ):
            if not _contains_any_of_words(
                    row[consts.COLUMN_DESCRIPTION],
                    ["rice", "pasta", "macaroni", "noodles", "spaghetti"],
            ):
                foods.drop(index, inplace=True)
                continue


def _add_columns(foods, food_nutrients):
    foods[consts.COLUMN_IS_BREAKFAST] = 0
    foods[consts.COLUMN_IS_MORNING_SNACK] = 0
    foods[consts.COLUMN_IS_LUNCH] = 0
    foods[consts.COLUMN_IS_AFTERNOON_SNACK] = 0
    foods[consts.COLUMN_IS_DINNER] = 0
    foods[consts.COLUMN_IS_BEVERAGE] = 0

    foods[consts.COLUMN_CALORIES] = None
    foods[consts.COLUMN_PROTEIN] = None
    foods[consts.COLUMN_FAT] = None
    foods[consts.COLUMN_CHOLESTEROL] = None
    foods[consts.COLUMN_CARBOHYDRATE] = None
    foods[consts.COLUMN_SUGAR] = None
    foods[consts.COLUMN_SODIUM] = None
    foods[consts.COLUMN_CALCIUM] = None
    foods[consts.COLUMN_IRON] = None
    foods[consts.COLUMN_POTASSIUM] = None
    foods[consts.COLUMN_VITAMIN_C] = None

    for index, row in foods.iterrows():
        # 1
        if row[consts.COLUMN_FOOD_CATEGORY_ID] in list(map(
                consts.category_id_mapper,
                consts.MEAL_FOOD_CATEGORY_MAPPING[consts.MEAL_BREAKFAST]
        )):
            foods.at[index, consts.COLUMN_IS_BREAKFAST] = 1

        if row[consts.COLUMN_FOOD_CATEGORY_ID] in list(map(
                consts.category_id_mapper,
                consts.MEAL_FOOD_CATEGORY_MAPPING[consts.MEAL_MORNING_SNACK]
        )):
            foods.at[index, consts.COLUMN_IS_MORNING_SNACK] = 1

        if row[consts.COLUMN_FOOD_CATEGORY_ID] in list(map(
                consts.category_id_mapper,
                consts.MEAL_FOOD_CATEGORY_MAPPING[consts.MEAL_LUNCH]
        )):
            foods.at[index, consts.COLUMN_IS_LUNCH] = 1

        if row[consts.COLUMN_FOOD_CATEGORY_ID] in list(map(
                consts.category_id_mapper,
                consts.MEAL_FOOD_CATEGORY_MAPPING[consts.MEAL_AFTERNOON_SNACK]
        )):
            foods.at[index, consts.COLUMN_IS_AFTERNOON_SNACK] = 1

        if row[consts.COLUMN_FOOD_CATEGORY_ID] in list(map(
                consts.category_id_mapper,
                consts.MEAL_FOOD_CATEGORY_MAPPING[consts.MEAL_DINNER]
        )):
            foods.at[index, consts.COLUMN_IS_DINNER] = 1

        if (
                (
                        row[consts.COLUMN_FOOD_CATEGORY_ID] ==
                        consts.category_id_mapper(consts.FOOD_CATEGORY_FRUITS_AND_FRUIT_JUICES) and
                        _contains_any_of_words(row[consts.COLUMN_DESCRIPTION], ["juice", "nectar"])
                ) or
                (
                        row[consts.COLUMN_FOOD_CATEGORY_ID] ==
                        consts.category_id_mapper(consts.FOOD_CATEGORY_BEVERAGES)
                )
        ):
            foods.at[index, consts.COLUMN_IS_BEVERAGE] = 1

        # 2
        fdc_id = row[consts.COLUMN_FDC_ID]
        current_food_nutrients = food_nutrients[food_nutrients[consts.COLUMN_FDC_ID] == fdc_id]
        food_nutrients = food_nutrients[food_nutrients[consts.COLUMN_FDC_ID] != fdc_id]

        for _, nutrients_row in current_food_nutrients.iterrows():
            for key in consts.NUTRITIONAL_ITEMS:
                if nutrients_row[consts.COLUMN_NUTRIENT_ID] == consts.NUTRITIONAL_ITEM_ID_MAPPING[key]:
                    foods.at[index, key] = nutrients_row[consts.COLUMN_AMOUNT]


def _contains_any_of_words(text: str, words: typing.List[str]):
    for word in words:
        if re.search(r"\b" + re.escape(word) + r"\b", text, flags=re.IGNORECASE):
            return True

    return False
