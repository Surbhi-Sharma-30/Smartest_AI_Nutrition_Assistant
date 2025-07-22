def calculate_bmr(gender, weight_kg, height_cm, age_years):
    """
    Calculates Basal Metabolic Rate (BMR) using the Mifflin-St Jeor Equation.
    :param gender: 'male' or 'female'.
    :param weight_kg: Weight in kilograms.
    :param height_cm: Height in centimeters.
    :param age_years: Age in years.
    :return: BMR in calories.
    """
    if gender.lower() == 'male':
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age_years) + 5
    elif gender.lower() == 'female':
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age_years) - 161
    else:
        return None 
    return bmr

def calculate_tdee(bmr, activity_level):
    """
    Calculates Total Daily Energy Expenditure (TDEE) based on BMR and activity level.
    :param bmr: Basal Metabolic Rate.
    :param activity_level: String representing activity level.
                           Options: 'sedentary', 'lightly active', 'moderately active',
                                    'very active', 'super active'.
    :return: TDEE in calories.
    """
    activity_factors = {
        "sedentary": 1.2, 
        "lightly active": 1.375, 
        "moderately active": 1.55,
        "very active": 1.725,
        "super active": 1.9
    }

    factor = activity_factors.get(activity_level.lower())
    if bmr is None or factor is None:
        return None

    tdee = bmr * factor
    return round(tdee, 2)

if __name__ == "__main__":
    gender = "male"
    weight = 75
    height = 180
    age = 30
    activity = "moderately active"

    bmr_val = calculate_bmr(gender, weight, height, age)
    if bmr_val:
        tdee_val = calculate_tdee(bmr_val, activity)
        if tdee_val:
            print(f"BMR: {bmr_val} calories/day")
            print(f"TDEE ({activity}): {tdee_val} calories/day")
        else:
            print("Invalid activity level.")
    else:
        print("Invalid gender.")
