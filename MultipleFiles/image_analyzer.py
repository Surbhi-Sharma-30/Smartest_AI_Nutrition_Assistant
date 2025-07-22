from gemini_api_handler import analyze_image_with_gemini

def analyze_food_image(image_file_buffer):
    """
    Analyzes a food image using the Gemini API.
    Delegates the core task to gemini_api_handler.
    """
    return analyze_image_with_gemini(image_file_buffer)

if __name__ == "__main__":
    pass

