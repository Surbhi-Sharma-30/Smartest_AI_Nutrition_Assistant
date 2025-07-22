from gemini_api_handler import get_gemini_response

def get_exercise_suggestions(goal, user_info=None):
    """
    Generates exercise suggestions based on the user's health goal and profile.
    :param goal: User's health goal (e.g., "Weight Loss", "Muscle Gain").
    :param user_info: Dictionary containing user details (name, age, weight, height, etc.).
    :return: String with exercise suggestions.
    """
    user_details = ""
    if user_info:
        user_details = f"Name: {user_info.get('name', 'User')}, Age: {user_info.get('age', 'N/A')} years, " \
                       f"Weight: {user_info.get('weight', 'N/A')} kg, Height: {user_info.get('height', 'N/A')} cm."

    prompt = f"""
    As an expert fitness coach, provide personalized exercise suggestions for a user with the following details:
    {user_details}
    Their primary health goal is: {goal}.

    Please provide:
    1. A brief introduction encouraging them.
    2. 3-5 specific exercise types or routines suitable for their goal (e.g., cardio, strength training, yoga).
    3. A sample weekly schedule or frequency recommendation.
    4. A note on safety and consistency.

    Keep the language encouraging and easy to understand.
    """
    return get_gemini_response(prompt)

if __name__ == "__main__":
    user_profile = {
        "name": "Alice",
        "age": 30,
        "weight": 65,
        "height": 165,
        "goal": "Weight Loss"
    }
    suggestions = get_exercise_suggestions(user_profile["goal"], user_profile)
    print("Exercise Suggestions:")
    print(suggestions)
