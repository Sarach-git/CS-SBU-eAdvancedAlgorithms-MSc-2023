import pulp

from django.utils.translation import gettext_lazy as _

from diet import consts
from diet.data import repository


def get_diet(gender, weight, height, age, lifestyle, goal, pregnant, lactating):
    bmr = calculate_bmr(gender, weight, height, age)
    tdee = calculate_tdee(bmr, lifestyle, pregnant, lactating)

    calories_range = calculate_calories(tdee, goal)

    protein_range = calculate_protein(gender, weight, lifestyle, goal, pregnant, lactating)

    fat_range = calculate_fat(gender, lifestyle, goal, calories_range)
    cholesterol_range = calculate_cholesterol()

    carbohydrate_range = calculate_carbohydrate(gender, lifestyle, goal, calories_range)
    sugar_range = calculate_sugar(calories_range)

    sodium_rage = calculate_sodium()
    calcium_range = calculate_calcium()
    iron_range = calculate_iron(gender, age, pregnant, lactating)
    potassium_range = calculate_potassium(age)
    vitamin_c_rage = calculate_vitamin_c(age, pregnant, lactating)

    diet = solve_lp(
        goal,
        {
            consts.NUTRITIONAL_ITEM_CALORIES: calories_range,
            consts.NUTRITIONAL_ITEM_PROTEIN: protein_range,
            consts.NUTRITIONAL_ITEM_FAT: fat_range,
            consts.NUTRITIONAL_ITEM_CHOLESTEROL: cholesterol_range,
            consts.NUTRITIONAL_ITEM_CARBOHYDRATE: carbohydrate_range,
            consts.NUTRITIONAL_ITEM_SUGAR: sugar_range,
            consts.NUTRITIONAL_ITEM_SODIUM: sodium_rage,
            consts.NUTRITIONAL_ITEM_CALCIUM: calcium_range,
            consts.NUTRITIONAL_ITEM_IRON: iron_range,
            consts.NUTRITIONAL_ITEM_POTASSIUM: potassium_range,
            consts.NUTRITIONAL_ITEM_VITAMIN_C: vitamin_c_rage,
        }
    )

    return {
        "numbers": {
            _("BMR"): bmr,
            _("TDEE"): tdee,
        },
        "ranges": {
            _(f"{consts.NUTRITIONAL_ITEM_NAME_MAPPING[consts.NUTRITIONAL_ITEM_CALORIES]} Range"): (
                calories_range,
                f"{consts.NUTRITIONAL_ITEM_UNIT_MAPPING[consts.NUTRITIONAL_ITEM_CALORIES]} per day",
            ),
            _(f"{consts.NUTRITIONAL_ITEM_NAME_MAPPING[consts.NUTRITIONAL_ITEM_PROTEIN]} Range"): (
                protein_range,
                f"{consts.NUTRITIONAL_ITEM_UNIT_MAPPING[consts.NUTRITIONAL_ITEM_PROTEIN]} per day",
            ),
            _(f"{consts.NUTRITIONAL_ITEM_NAME_MAPPING[consts.NUTRITIONAL_ITEM_FAT]} Range"): (
                fat_range,
                f"{consts.NUTRITIONAL_ITEM_UNIT_MAPPING[consts.NUTRITIONAL_ITEM_FAT]} per day",
            ),
            _(f"{consts.NUTRITIONAL_ITEM_NAME_MAPPING[consts.NUTRITIONAL_ITEM_CHOLESTEROL]} Range"): (
                cholesterol_range,
                f"{consts.NUTRITIONAL_ITEM_UNIT_MAPPING[consts.NUTRITIONAL_ITEM_CHOLESTEROL]} per day",
            ),
            _(f"{consts.NUTRITIONAL_ITEM_NAME_MAPPING[consts.NUTRITIONAL_ITEM_CARBOHYDRATE]} Range"): (
                carbohydrate_range,
                f"{consts.NUTRITIONAL_ITEM_UNIT_MAPPING[consts.NUTRITIONAL_ITEM_CARBOHYDRATE]} per day",
            ),
            _(f"{consts.NUTRITIONAL_ITEM_NAME_MAPPING[consts.NUTRITIONAL_ITEM_SUGAR]} Range"): (
                sugar_range,
                f"{consts.NUTRITIONAL_ITEM_UNIT_MAPPING[consts.NUTRITIONAL_ITEM_SUGAR]} per day",
            ),
            _(f"{consts.NUTRITIONAL_ITEM_NAME_MAPPING[consts.NUTRITIONAL_ITEM_CALCIUM]} Range"): (
                calcium_range,
                f"{consts.NUTRITIONAL_ITEM_UNIT_MAPPING[consts.NUTRITIONAL_ITEM_CALCIUM]} per day",
            ),
            _(f"{consts.NUTRITIONAL_ITEM_NAME_MAPPING[consts.NUTRITIONAL_ITEM_SODIUM]} Range"): (
                sodium_rage,
                f"{consts.NUTRITIONAL_ITEM_UNIT_MAPPING[consts.NUTRITIONAL_ITEM_SODIUM]} per day",
            ),
            _(f"{consts.NUTRITIONAL_ITEM_NAME_MAPPING[consts.NUTRITIONAL_ITEM_IRON]} Range"): (
                iron_range,
                f"{consts.NUTRITIONAL_ITEM_UNIT_MAPPING[consts.NUTRITIONAL_ITEM_IRON]} per day",
            ),
            _(f"{consts.NUTRITIONAL_ITEM_NAME_MAPPING[consts.NUTRITIONAL_ITEM_POTASSIUM]} Range"): (
                potassium_range,
                f"{consts.NUTRITIONAL_ITEM_UNIT_MAPPING[consts.NUTRITIONAL_ITEM_POTASSIUM]} per day",
            ),
            _(f"{consts.NUTRITIONAL_ITEM_NAME_MAPPING[consts.NUTRITIONAL_ITEM_VITAMIN_C]} Range"): (
                vitamin_c_rage,
                f"{consts.NUTRITIONAL_ITEM_UNIT_MAPPING[consts.NUTRITIONAL_ITEM_VITAMIN_C]} per day",
            ),
        },
        "diet": diet,
    }


def calculate_bmr(gender, weight, height, age):
    if gender == consts.GENDER_FEMALE:
        return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    if gender == consts.GENDER_MALE:
        return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)


def calculate_tdee(bmr, lifestyle, pregnant, lactating):
    factor = 1

    if pregnant:
        factor *= 1.2

    if lactating:
        factor *= 1.5

    if lifestyle == consts.LIFESTYLE_SEDENTARY:
        return bmr * 1.2
    if lifestyle == consts.LIFESTYLE_SLIGHTLY_ACTIVE:
        return bmr * 1.375
    if lifestyle == consts.LIFESTYLE_MODERATELY_ACTIVE:
        return bmr * 1.55
    if lifestyle == consts.LIFESTYLE_VERY_ACTIVE:
        return bmr * 1.725
    if lifestyle == consts.LIFESTYLE_EXTREMELY_ACTIVE:
        return bmr * 1.9


def calculate_calories(tdee, goal):
    if goal == consts.GOAL_MAINTENANCE:
        return tdee * 0.9, tdee * 1.1

    if goal == consts.GOAL_MUSCLE_GAIN:
        return tdee * 1.1, tdee * 1.2

    if goal == consts.GOAL_FAT_LOSS:
        return tdee * 0.8, tdee * 0.9


def calculate_protein(gender, weight, lifestyle, goal, pregnant, lactating):
    min_per_kg_body_wight, max_per_kg_body_wight = {
        (consts.GENDER_MALE, consts.LIFESTYLE_SEDENTARY, consts.GOAL_MAINTENANCE): (0.8, 1.0),
        (consts.GENDER_MALE, consts.LIFESTYLE_SEDENTARY, consts.GOAL_MUSCLE_GAIN): (1.2, 1.5),
        (consts.GENDER_MALE, consts.LIFESTYLE_SEDENTARY, consts.GOAL_FAT_LOSS): (1.2, 1.5),
        (consts.GENDER_MALE, consts.LIFESTYLE_SLIGHTLY_ACTIVE, consts.GOAL_MAINTENANCE): (0.8, 1.2),
        (consts.GENDER_MALE, consts.LIFESTYLE_SLIGHTLY_ACTIVE, consts.GOAL_MUSCLE_GAIN): (1.2, 1.7),
        (consts.GENDER_MALE, consts.LIFESTYLE_SLIGHTLY_ACTIVE, consts.GOAL_FAT_LOSS): (1.2, 1.7),
        (consts.GENDER_MALE, consts.LIFESTYLE_MODERATELY_ACTIVE, consts.GOAL_MAINTENANCE): (1.0, 1.2),
        (consts.GENDER_MALE, consts.LIFESTYLE_MODERATELY_ACTIVE, consts.GOAL_MUSCLE_GAIN): (1.5, 1.7),
        (consts.GENDER_MALE, consts.LIFESTYLE_MODERATELY_ACTIVE, consts.GOAL_FAT_LOSS): (1.5, 1.7),
        (consts.GENDER_MALE, consts.LIFESTYLE_VERY_ACTIVE, consts.GOAL_MAINTENANCE): (1.0, 1.5),
        (consts.GENDER_MALE, consts.LIFESTYLE_VERY_ACTIVE, consts.GOAL_MUSCLE_GAIN): (1.5, 2.0),
        (consts.GENDER_MALE, consts.LIFESTYLE_VERY_ACTIVE, consts.GOAL_FAT_LOSS): (1.5, 1.7),
        (consts.GENDER_MALE, consts.LIFESTYLE_EXTREMELY_ACTIVE, consts.GOAL_MAINTENANCE): (1.2, 1.5),
        (consts.GENDER_MALE, consts.LIFESTYLE_EXTREMELY_ACTIVE, consts.GOAL_MUSCLE_GAIN): (1.7, 2.0),
        (consts.GENDER_MALE, consts.LIFESTYLE_EXTREMELY_ACTIVE, consts.GOAL_FAT_LOSS): (1.5, 1.7),

        (consts.GENDER_FEMALE, consts.LIFESTYLE_SEDENTARY, consts.GOAL_MAINTENANCE): (0.8, 1.0),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_SEDENTARY, consts.GOAL_MUSCLE_GAIN): (1.0, 1.2),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_SEDENTARY, consts.GOAL_FAT_LOSS): (1.0, 1.2),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_SLIGHTLY_ACTIVE, consts.GOAL_MAINTENANCE): (0.8, 1.0),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_SLIGHTLY_ACTIVE, consts.GOAL_MUSCLE_GAIN): (1.0, 1.5),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_SLIGHTLY_ACTIVE, consts.GOAL_FAT_LOSS): (1.0, 1.5),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_MODERATELY_ACTIVE, consts.GOAL_MAINTENANCE): (0.8, 1.0),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_MODERATELY_ACTIVE, consts.GOAL_MUSCLE_GAIN): (1.2, 1.5),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_MODERATELY_ACTIVE, consts.GOAL_FAT_LOSS): (1.2, 1.5),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_VERY_ACTIVE, consts.GOAL_MAINTENANCE): (0.8, 1.2),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_VERY_ACTIVE, consts.GOAL_MUSCLE_GAIN): (1.2, 1.7),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_VERY_ACTIVE, consts.GOAL_FAT_LOSS): (1.2, 1.5),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_EXTREMELY_ACTIVE, consts.GOAL_MAINTENANCE): (1.0, 1.2),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_EXTREMELY_ACTIVE, consts.GOAL_MUSCLE_GAIN): (1.5, 1.7),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_EXTREMELY_ACTIVE, consts.GOAL_FAT_LOSS): (1.2, 1.5),
    }[gender, lifestyle, goal]

    if pregnant:
        min_per_kg_body_wight += 0.3
        max_per_kg_body_wight += 0.4

    if lactating:
        min_per_kg_body_wight += 0.2
        max_per_kg_body_wight += 0.3

    return min_per_kg_body_wight * weight, max_per_kg_body_wight * weight


def calculate_fat(gender, lifestyle, goal, calories_range):
    fat_percentage = {
        (consts.GENDER_MALE, consts.LIFESTYLE_SEDENTARY, consts.GOAL_MAINTENANCE): (20, 25),
        (consts.GENDER_MALE, consts.LIFESTYLE_SEDENTARY, consts.GOAL_MUSCLE_GAIN): (20, 30),
        (consts.GENDER_MALE, consts.LIFESTYLE_SEDENTARY, consts.GOAL_FAT_LOSS): (20, 30),
        (consts.GENDER_MALE, consts.LIFESTYLE_SLIGHTLY_ACTIVE, consts.GOAL_MAINTENANCE): (25, 30),
        (consts.GENDER_MALE, consts.LIFESTYLE_SLIGHTLY_ACTIVE, consts.GOAL_MUSCLE_GAIN): (20, 30),
        (consts.GENDER_MALE, consts.LIFESTYLE_SLIGHTLY_ACTIVE, consts.GOAL_FAT_LOSS): (20, 30),
        (consts.GENDER_MALE, consts.LIFESTYLE_MODERATELY_ACTIVE, consts.GOAL_MAINTENANCE): (30, 35),
        (consts.GENDER_MALE, consts.LIFESTYLE_MODERATELY_ACTIVE, consts.GOAL_MUSCLE_GAIN): (20, 30),
        (consts.GENDER_MALE, consts.LIFESTYLE_MODERATELY_ACTIVE, consts.GOAL_FAT_LOSS): (20, 30),
        (consts.GENDER_MALE, consts.LIFESTYLE_VERY_ACTIVE, consts.GOAL_MAINTENANCE): (35, 40),
        (consts.GENDER_MALE, consts.LIFESTYLE_VERY_ACTIVE, consts.GOAL_MUSCLE_GAIN): (20, 30),
        (consts.GENDER_MALE, consts.LIFESTYLE_VERY_ACTIVE, consts.GOAL_FAT_LOSS): (20, 30),
        (consts.GENDER_MALE, consts.LIFESTYLE_EXTREMELY_ACTIVE, consts.GOAL_MAINTENANCE): (40, 45),
        (consts.GENDER_MALE, consts.LIFESTYLE_EXTREMELY_ACTIVE, consts.GOAL_MUSCLE_GAIN): (20, 30),
        (consts.GENDER_MALE, consts.LIFESTYLE_EXTREMELY_ACTIVE, consts.GOAL_FAT_LOSS): (20, 30),

        (consts.GENDER_FEMALE, consts.LIFESTYLE_SEDENTARY, consts.GOAL_MAINTENANCE): (20, 25),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_SEDENTARY, consts.GOAL_MUSCLE_GAIN): (20, 30),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_SEDENTARY, consts.GOAL_FAT_LOSS): (20, 30),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_SLIGHTLY_ACTIVE, consts.GOAL_MAINTENANCE): (25, 30),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_SLIGHTLY_ACTIVE, consts.GOAL_MUSCLE_GAIN): (20, 30),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_SLIGHTLY_ACTIVE, consts.GOAL_FAT_LOSS): (20, 30),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_MODERATELY_ACTIVE, consts.GOAL_MAINTENANCE): (30, 35),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_MODERATELY_ACTIVE, consts.GOAL_MUSCLE_GAIN): (20, 30),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_MODERATELY_ACTIVE, consts.GOAL_FAT_LOSS): (20, 30),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_VERY_ACTIVE, consts.GOAL_MAINTENANCE): (35, 40),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_VERY_ACTIVE, consts.GOAL_MUSCLE_GAIN): (20, 30),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_VERY_ACTIVE, consts.GOAL_FAT_LOSS): (20, 30),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_EXTREMELY_ACTIVE, consts.GOAL_MAINTENANCE): (40, 45),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_EXTREMELY_ACTIVE, consts.GOAL_MUSCLE_GAIN): (20, 30),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_EXTREMELY_ACTIVE, consts.GOAL_FAT_LOSS): (20, 30),
    }[gender, lifestyle, goal]

    # Convert calories to grams (1 gram of fat = 9 calories)
    return (fat_percentage[0] / 100) * calories_range[0] / 9, (fat_percentage[1] / 100) * calories_range[1] / 9


def calculate_cholesterol():
    return 200, 300


def calculate_carbohydrate(gender, lifestyle, goal, calories_range):
    carbohydrate_percentage = {
        (consts.GENDER_MALE, consts.LIFESTYLE_SEDENTARY, consts.GOAL_MAINTENANCE): (50, 65),
        (consts.GENDER_MALE, consts.LIFESTYLE_SEDENTARY, consts.GOAL_MUSCLE_GAIN): (45, 65),
        (consts.GENDER_MALE, consts.LIFESTYLE_SEDENTARY, consts.GOAL_FAT_LOSS): (45, 65),
        (consts.GENDER_MALE, consts.LIFESTYLE_SLIGHTLY_ACTIVE, consts.GOAL_MAINTENANCE): (45, 60),
        (consts.GENDER_MALE, consts.LIFESTYLE_SLIGHTLY_ACTIVE, consts.GOAL_MUSCLE_GAIN): (45, 65),
        (consts.GENDER_MALE, consts.LIFESTYLE_SLIGHTLY_ACTIVE, consts.GOAL_FAT_LOSS): (45, 65),
        (consts.GENDER_MALE, consts.LIFESTYLE_MODERATELY_ACTIVE, consts.GOAL_MAINTENANCE): (40, 55),
        (consts.GENDER_MALE, consts.LIFESTYLE_MODERATELY_ACTIVE, consts.GOAL_MUSCLE_GAIN): (45, 65),
        (consts.GENDER_MALE, consts.LIFESTYLE_MODERATELY_ACTIVE, consts.GOAL_FAT_LOSS): (45, 65),
        (consts.GENDER_MALE, consts.LIFESTYLE_VERY_ACTIVE, consts.GOAL_MAINTENANCE): (35, 50),
        (consts.GENDER_MALE, consts.LIFESTYLE_VERY_ACTIVE, consts.GOAL_MUSCLE_GAIN): (45, 65),
        (consts.GENDER_MALE, consts.LIFESTYLE_VERY_ACTIVE, consts.GOAL_FAT_LOSS): (45, 65),
        (consts.GENDER_MALE, consts.LIFESTYLE_EXTREMELY_ACTIVE, consts.GOAL_MAINTENANCE): (30, 45),
        (consts.GENDER_MALE, consts.LIFESTYLE_EXTREMELY_ACTIVE, consts.GOAL_MUSCLE_GAIN): (45, 65),
        (consts.GENDER_MALE, consts.LIFESTYLE_EXTREMELY_ACTIVE, consts.GOAL_FAT_LOSS): (45, 65),

        (consts.GENDER_FEMALE, consts.LIFESTYLE_SEDENTARY, consts.GOAL_MAINTENANCE): (50, 65),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_SEDENTARY, consts.GOAL_MUSCLE_GAIN): (45, 65),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_SEDENTARY, consts.GOAL_FAT_LOSS): (45, 65),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_SLIGHTLY_ACTIVE, consts.GOAL_MAINTENANCE): (45, 60),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_SLIGHTLY_ACTIVE, consts.GOAL_MUSCLE_GAIN): (45, 65),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_SLIGHTLY_ACTIVE, consts.GOAL_FAT_LOSS): (45, 65),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_MODERATELY_ACTIVE, consts.GOAL_MAINTENANCE): (40, 55),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_MODERATELY_ACTIVE, consts.GOAL_MUSCLE_GAIN): (45, 65),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_MODERATELY_ACTIVE, consts.GOAL_FAT_LOSS): (45, 65),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_VERY_ACTIVE, consts.GOAL_MAINTENANCE): (35, 50),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_VERY_ACTIVE, consts.GOAL_MUSCLE_GAIN): (45, 65),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_VERY_ACTIVE, consts.GOAL_FAT_LOSS): (45, 65),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_EXTREMELY_ACTIVE, consts.GOAL_MAINTENANCE): (30, 45),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_EXTREMELY_ACTIVE, consts.GOAL_MUSCLE_GAIN): (45, 65),
        (consts.GENDER_FEMALE, consts.LIFESTYLE_EXTREMELY_ACTIVE, consts.GOAL_FAT_LOSS): (45, 65),
    }[gender, lifestyle, goal]

    # Convert calories to grams (1 gram of carbohydrate = 4 calories)
    return (
        (carbohydrate_percentage[0] / 100) * calories_range[0] / 4,
        (carbohydrate_percentage[1] / 100) * calories_range[1] / 4
    )


def calculate_sugar(calories_range):
    # It is advised to limit sugar intake to no more than 10% of total daily calorie intake.
    # Convert calories to grams (1 gram of carbohydrate = 4 calories)
    return 0, (10 / 100) * calories_range[1] / 4


def calculate_sodium():
    return 200, 2300


def calculate_calcium():
    return 1000, 1200


def calculate_iron(gender, age, pregnant, lactating):
    if age <= 3:
        return 7, 11

    if age <= 8:
        return 10, 14

    if age <= 13:
        return 8, 12

    if age <= 18:
        if gender == consts.GENDER_MALE:
            return 11, 15

        if gender == consts.GENDER_FEMALE:
            if pregnant:
                return 27, 31

            if lactating:
                return 10, 14

            return 15, 19

    if age <= 50:
        if gender == consts.GENDER_MALE:
            return 8, 12

        if gender == consts.GENDER_FEMALE:
            if pregnant:
                return 27, 31

            if lactating:
                return 9, 13

            return 18, 22

    return 8, 12


def calculate_potassium(age):
    if age <= 3:
        return 2000, 2500

    if age <= 8:
        return 2300, 2900

    if age <= 13:
        return 2500, 3000

    if age <= 18:
        return 2600, 3000

    return 2600, 3400


def calculate_vitamin_c(age, pregnant, lactating):
    if age <= 3:
        return 15, 35

    if age <= 8:
        return 25, 45

    if age <= 13:
        return 45, 65

    if pregnant and lactating:
        return 120, 130

    if pregnant:
        return 80, 95

    if lactating:
        return 115, 120

    return 75, 90


def solve_lp(goal, ranges):
    foods = repository.get_foods()
    foods_mapping = repository.get_foods_mapping()
    food_ids = foods[consts.COLUMN_FDC_ID].tolist()

    prob = pulp.LpProblem(
        "DietOptimization",
        pulp.LpMinimize if goal == consts.GOAL_FAT_LOSS else pulp.LpMaximize
    )

    # define variables
    v = {
        "b": pulp.LpVariable.dicts("b", food_ids, lowBound=0, cat=pulp.const.LpContinuous),
        "m": pulp.LpVariable.dicts("m", food_ids, lowBound=0, cat=pulp.const.LpContinuous),
        "l": pulp.LpVariable.dicts("l", food_ids, lowBound=0, cat=pulp.const.LpContinuous),
        "a": pulp.LpVariable.dicts("a", food_ids, lowBound=0, cat=pulp.const.LpContinuous),
        "d": pulp.LpVariable.dicts("d", food_ids, lowBound=0, cat=pulp.const.LpContinuous),
        "x": pulp.LpVariable.dicts("x", food_ids, lowBound=0, cat=pulp.const.LpContinuous),

        "bc": pulp.LpVariable.dicts("bc", food_ids, lowBound=0, cat=pulp.const.LpBinary),
        "mc": pulp.LpVariable.dicts("mc", food_ids, lowBound=0, cat=pulp.const.LpBinary),
        "lc": pulp.LpVariable.dicts("lc", food_ids, lowBound=0, cat=pulp.const.LpBinary),
        "ac": pulp.LpVariable.dicts("ac", food_ids, lowBound=0, cat=pulp.const.LpBinary),
        "dc": pulp.LpVariable.dicts("dc", food_ids, lowBound=0, cat=pulp.const.LpBinary),
    }

    if goal == consts.GOAL_FAT_LOSS:
        # minimize calories
        prob += pulp.lpSum((foods[consts.COLUMN_CALORIES][i] / 100) * v["x"][fid] for i, fid in enumerate(food_ids))
    else:
        # maximize protein
        prob += pulp.lpSum((foods[consts.COLUMN_PROTEIN][i] / 100) * v["x"][fid] for i, fid in enumerate(food_ids))

    # constraints relating food variables and meal variables
    for fid in food_ids:
        prob += pulp.lpSum((v["b"][fid], v["m"][fid], v["l"][fid], v["a"][fid], v["d"][fid])) == v["x"][fid]

    # constraints for either not having a food or having between MIN_FOOD and MAX_FOOD grams of the food in each meal
    # mc is one if m is none-zero and is zero if m is zero for m in {b, m, l, a, d}
    for fid in food_ids:
        prob += v["b"][fid] <= consts.MAX_FOOD * v["bc"][fid]
        prob += v["b"][fid] >= consts.MIN_FOOD * v["bc"][fid]

        prob += v["m"][fid] <= consts.MAX_FOOD * v["mc"][fid]
        prob += v["m"][fid] >= consts.MIN_FOOD * v["mc"][fid]

        prob += v["l"][fid] <= consts.MAX_FOOD * v["lc"][fid]
        prob += v["l"][fid] >= consts.MIN_FOOD * v["lc"][fid]

        prob += v["a"][fid] <= consts.MAX_FOOD * v["ac"][fid]
        prob += v["a"][fid] >= consts.MIN_FOOD * v["ac"][fid]

        prob += v["d"][fid] <= consts.MAX_FOOD * v["dc"][fid]
        prob += v["d"][fid] >= consts.MIN_FOOD * v["dc"][fid]

    # constraints for not repeating a food in two meals
    for fid in food_ids:
        prob += pulp.lpSum((v["bc"][fid], v["mc"][fid], v["lc"][fid], v["ac"][fid], v["dc"][fid])) <= 1

    # constraints for excluding non-relevant foods in meals
    for i, fid in enumerate(food_ids):
        if not foods[consts.COLUMN_IS_BREAKFAST][i]:
            prob += v["b"][fid] == 0

        if not foods[consts.COLUMN_IS_MORNING_SNACK][i]:
            prob += v["m"][fid] == 0

        if not foods[consts.COLUMN_IS_LUNCH][i]:
            prob += v["l"][fid] == 0

        if not foods[consts.COLUMN_IS_AFTERNOON_SNACK][i]:
            prob += v["a"][fid] == 0

        if not foods[consts.COLUMN_IS_DINNER][i]:
            prob += v["d"][fid] == 0

    # constraints for food and beverage intake per meal and per day
    is_beverage = foods[consts.COLUMN_IS_BEVERAGE]

    prob += pulp.lpSum((1 - is_beverage[i]) * v["b"][fid] for i, fid in enumerate(food_ids)) >= consts.MIN_MEAL_FOOD
    prob += pulp.lpSum((1 - is_beverage[i]) * v["b"][fid] for i, fid in enumerate(food_ids)) <= consts.MAX_MEAL_FOOD

    prob += pulp.lpSum((1 - is_beverage[i]) * v["m"][fid] for i, fid in enumerate(food_ids)) >= consts.MIN_SNACK_FOOD
    prob += pulp.lpSum((1 - is_beverage[i]) * v["m"][fid] for i, fid in enumerate(food_ids)) <= consts.MAX_SNACK_FOOD

    prob += pulp.lpSum((1 - is_beverage[i]) * v["l"][fid] for i, fid in enumerate(food_ids)) >= consts.MIN_MEAL_FOOD
    prob += pulp.lpSum((1 - is_beverage[i]) * v["l"][fid] for i, fid in enumerate(food_ids)) <= consts.MAX_MEAL_FOOD

    prob += pulp.lpSum((1 - is_beverage[i]) * v["a"][fid] for i, fid in enumerate(food_ids)) >= consts.MIN_SNACK_FOOD
    prob += pulp.lpSum((1 - is_beverage[i]) * v["a"][fid] for i, fid in enumerate(food_ids)) <= consts.MAX_SNACK_FOOD

    prob += pulp.lpSum((1 - is_beverage[i]) * v["d"][fid] for i, fid in enumerate(food_ids)) >= consts.MIN_MEAL_FOOD
    prob += pulp.lpSum((1 - is_beverage[i]) * v["d"][fid] for i, fid in enumerate(food_ids)) <= consts.MAX_MEAL_FOOD

    prob += pulp.lpSum(is_beverage[i] * v["b"][fid] for i, fid in enumerate(food_ids)) >= consts.MIN_MEAL_BEVERAGE
    prob += pulp.lpSum(is_beverage[i] * v["b"][fid] for i, fid in enumerate(food_ids)) <= consts.MAX_MEAL_BEVERAGE

    prob += pulp.lpSum(is_beverage[i] * v["m"][fid] for i, fid in enumerate(food_ids)) >= consts.MIN_SNACK_BEVERAGE
    prob += pulp.lpSum(is_beverage[i] * v["m"][fid] for i, fid in enumerate(food_ids)) <= consts.MAX_SNACK_BEVERAGE

    prob += pulp.lpSum(is_beverage[i] * v["l"][fid] for i, fid in enumerate(food_ids)) >= consts.MIN_MEAL_BEVERAGE
    prob += pulp.lpSum(is_beverage[i] * v["l"][fid] for i, fid in enumerate(food_ids)) <= consts.MAX_MEAL_BEVERAGE

    prob += pulp.lpSum(is_beverage[i] * v["a"][fid] for i, fid in enumerate(food_ids)) >= consts.MIN_SNACK_BEVERAGE
    prob += pulp.lpSum(is_beverage[i] * v["a"][fid] for i, fid in enumerate(food_ids)) <= consts.MAX_SNACK_BEVERAGE

    prob += pulp.lpSum(is_beverage[i] * v["d"][fid] for i, fid in enumerate(food_ids)) >= consts.MIN_MEAL_BEVERAGE
    prob += pulp.lpSum(is_beverage[i] * v["d"][fid] for i, fid in enumerate(food_ids)) <= consts.MAX_MEAL_BEVERAGE

    # nutrient constraints
    for key in consts.NUTRITIONAL_ITEMS:
        prob += pulp.lpSum((foods[key][i] / 100) * v["x"][fid] for i, fid in enumerate(food_ids)) >= ranges[key][0]
        prob += pulp.lpSum((foods[key][i] / 100) * v["x"][fid] for i, fid in enumerate(food_ids)) <= ranges[key][1]

    # solve the problem
    prob.solve()

    # prepare result
    result = {
        "status": pulp.LpStatus[prob.status],
        "nutritional_items": [],
    }

    for item in consts.NUTRITIONAL_ITEMS:
        result["nutritional_items"].append({
            "name": consts.NUTRITIONAL_ITEM_NAME_MAPPING[item],
            "value": str(int(sum(
                (foods[item][i] / 100) * v["x"][food_id].varValue for i, food_id in enumerate(food_ids)
            ))) + " " + consts.NUTRITIONAL_ITEM_UNIT_MAPPING[item],
        })

    result["meals"] = []
    for meal in consts.MEALS:
        print(
            list(f"{int(v[consts.MEAL_VAR_MAPPING[meal]][food_id].varValue)} grams {foods_mapping[food_id]}"
            for food_id in food_ids if v[consts.MEAL_VAR_MAPPING[meal]][food_id].varValue != 0)
        )

        result["meals"].append({
            "name": consts.MEAL_NAME_MAPPING[meal],
            "value": [
                f"{int(v[consts.MEAL_VAR_MAPPING[meal]][food_id].varValue)} grams {foods_mapping[food_id]}"
                for food_id in food_ids if v[consts.MEAL_VAR_MAPPING[meal]][food_id].varValue != 0
            ],
        })

    return result
