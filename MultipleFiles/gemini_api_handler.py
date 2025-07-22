import google.generativeai as genai
from dotenv import load_dotenv
import os
from PIL import Image
import io

load_dotenv()

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(
    api_key=GEMINI_API_KEY,
    client_options={"api_endpoint": "generativelanguage.googleapis.com"}
)


def get_gemini_response(prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"I couldn't generate a response. Error: {str(e)}"

def analyze_image_with_gemini(image_file):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        img = Image.open(io.BytesIO(image_file.read()))
        
        prompt = """Analyze this food image and provide:
        1. Food items identified
        2. Estimated calories
        3. Macronutrient breakdown
        4. Healthiness score (1-10)
        5. Dietary compatibility
        
        Respond in clear bullet points."""
        
        response = model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        return f"Image analysis failed: {str(e)}"

# check_available_models() # <--- You might comment this out if it causes startup issues