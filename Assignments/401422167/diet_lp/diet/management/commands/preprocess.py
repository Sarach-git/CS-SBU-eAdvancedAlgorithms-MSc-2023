import pathlib

from django.core.management import BaseCommand

import pandas as pd

from diet.data.preprocess import preprocess


class Command(BaseCommand):
    help = "Preprocess the dataset"

    def add_arguments(self, parser):
        parser.add_argument("input", help="Input directory name")
        parser.add_argument("output", help="Output CSV file name")

    def handle(self, *args, **options):
        input_dir = pathlib.Path(options["input"])

        foods = pd.read_csv(input_dir / "food.csv")

        food_nutrients = pd.read_csv(input_dir / "food_nutrient.csv")

        foods = preprocess(foods, food_nutrients)

        foods.to_csv(options["output"], index=False)
