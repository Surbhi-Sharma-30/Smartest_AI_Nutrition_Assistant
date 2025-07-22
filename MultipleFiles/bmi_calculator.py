def calculate_bmi(weight_kg, height_cm):
    """
    Calculates Body Mass Index (BMI).
    :param weight_kg: Weight in kilograms.
    :param height_cm: Height in centimeters.
    :return: BMI value and category.
    """
    if height_cm <= 0:
        return None, "Height must be greater than 0."

    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)

    category = ""
    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 24.9:
        category = "Normal weight"
    elif 25 <= bmi < 29.9:
        category = "Overweight"
    else:
        category = "Obesity"

    return round(bmi, 2), category
if __name__ == "__main__":
    bmi_val, bmi_cat = calculate_bmi(70, 175)
    if bmi_val:
        print(f"BMI: {bmi_val}, Category: {bmi_cat}")
    else:
        print(bmi_cat)
