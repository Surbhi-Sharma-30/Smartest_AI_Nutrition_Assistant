import streamlit as st
import os
from dotenv import load_dotenv
from gemini_api_handler import get_gemini_response, analyze_image_with_gemini
from voice_to_text import transcribe_microphone
from csv_handler import save_user_response
import io
import pandas as pd
import base64
from bmi_calculator import calculate_bmi
from calorie_calculator import calculate_bmr, calculate_tdee
from exercise_suggestions import get_exercise_suggestions

# Load environment variables
load_dotenv()

# BACKGROUND IMAGE SETUP
def get_base64_image(image_path):
    """Convert image file to base64 string"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except FileNotFoundError:
        return None

BACKGROUND_IMAGE_PATH = "NutriAI.jpg" 

# Load the background image
background_image_base64 = get_base64_image(BACKGROUND_IMAGE_PATH)
if background_image_base64 is None:
    st.warning(f"Background image not found at {BACKGROUND_IMAGE_PATH}. Using default styling.")



# CUSTOM CSS STYLING
def set_custom_style():
    if background_image_base64:
        st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
        
        * {{
            font-family: 'Poppins', sans-serif;
        }}

        .stApp {{
            background-image: url("data:image/jpg;base64,{background_image_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-color: rgba(255, 255, 255, 0.7);
            background-blend-mode: overlay;
        }}
        .stSidebar > div:first-child {{
            background-color: rgba(255, 255, 255, 0.85);
            border-right: 1px solid rgba(0,0,0,0.1);
        }}
        .main .block-container {{
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        .stButton>button {{
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 10px 25px;
            font-size: 16px;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }}
        .stButton>button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        }}
        .gradient-text {{
            background: linear-gradient(90deg, #3b82f6, #6366f1, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: inline-block;
        }}
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
        
        * {{
            font-family: 'Poppins', sans-serif;
        }}
        .stApp {
            background-color: #f0f2f6;
        }
        .stSidebar > div:first-child {
            background-color: rgba(255, 255, 255, 0.85);
        }
        .main .block-container {
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .stButton>button {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 10px 25px;
            font-size: 16px;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }}
        .stButton>button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        }}
        .gradient-text {{
            background: linear-gradient(90deg, #3b82f6, #6366f1, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: inline-block;
        }}
        </style>
        """, unsafe_allow_html=True)

# SESSION STATE INITIALIZATION
if 'user_info' not in st.session_state:
    st.session_state.user_info = {
        "name": "",
        "age": 30,
        "weight": 70,
        "height": 170,
        "gender": "male",
        "activity_level": "moderately active",
        "goal": "Weight Loss",
        "diet": "Balanced",
        "allergies": [],
        "restrictions": [],
        "meals_per_day": 3,
        "snacks_per_day": 1
    }

if 'last_response' not in st.session_state:
    st.session_state.last_response = ""

#Apply custom styles
set_custom_style()

# App Header
st.markdown("""
<div style="text-align:center; margin-bottom: 40px;">
    <h1 class="gradient-text">Smartest Nutrition AI Assistant</h1>
    <p>Get instant nutrition advice, calculate your needs, and find exercise suggestions!</p>
</div>
""", unsafe_allow_html=True)

# User Profile Section
with st.sidebar:
    st.header("👤 Your Profile")
    st.session_state.user_info["name"] = st.text_input("Name", value=st.session_state.user_info["name"])
    st.session_state.user_info["age"] = st.number_input("Age", min_value=1, max_value=100, value=st.session_state.user_info["age"])
    st.session_state.user_info["gender"] = st.selectbox("Gender", ["Male", "Female", "Other"], index=0 if st.session_state.user_info["gender"].lower() == "male" else 1)
    st.session_state.user_info["weight"] = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=float(st.session_state.user_info["weight"]))
    st.session_state.user_info["height"] = st.number_input("Height (cm)", min_value=1.0, max_value=250.0, value=float(st.session_state.user_info["height"]))
    st.session_state.user_info["goal"] = st.selectbox(
        "Health Goal",
        ["Weight Loss","Muscle Gain","Maintain Weight","Improve Health","Heart Health","Diabetes Management","Better Digestion","Boost Immunity","Mental Wellbeing","Plant-Based/Vegan Nutrition",
         "Allergy-Aware Eating","Sports Nutrition","Healthy Aging","Hormonal Balance","PMS/PCOS-Friendly Nutrition","Pregnancy Nutrition","Child Nutrition","Skin Health"]
    )
    st.session_state.user_info["activity_level"] = st.selectbox(
        "Activity Level",
        ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Super Active"]
    )
    st.session_state.user_info["diet"] = st.selectbox(
        "Preferred Diet",
        ["Balanced", "Paleo", "Vegan", "Keto", "Mediterranean", "Vegetarian", "Low Carb", "High Protein", "Gluten-Free", "Dairy-Free", "Low FODMAP", "Whole30", "Raw Food", "Intermittent Fasting",
         "Ayurvedic", "Dash Diet", "Carnivore", "Flexitarian", "Diabetic-Friendly", "Non-Vegetarian", "Pescatarian"]
    )
    st.session_state.user_info["allergies"] = st.multiselect(
        "Allergies",
        ["Peanuts", "Tree Nuts", "Dairy", "Gluten", "Soy", "Eggs", "Fish", "Sesame", "Corn", "Sulphites"],
        default=st.session_state.user_info["allergies"]
    )
    st.session_state.user_info["restrictions"] = st.multiselect(
        "Dietary Restrictions",
        ["Vegan", "Vegetarian", "Keto", "Low Carb", "Sugar-Free"],
        default=st.session_state.user_info["restrictions"]
    )
    st.session_state.user_info["meals_per_day"] = st.number_input(
        "Meals per day", min_value=1, max_value=6, value=st.session_state.user_info["meals_per_day"]
    )
    st.session_state.user_info["snacks_per_day"] = st.number_input(
        "Snacks per day", min_value=0, max_value=4, value=st.session_state.user_info["snacks_per_day"]
    )

# Main content tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["AI Chat", "Voice Input", "Image Analysis", "Calculators", "Exercise Suggestions"])

#AI Chat Tab
with tab1:
    st.subheader("Ask Your Nutrition Question")
    user_query_tab1 = st.text_area("Type your question here:", height=100)
    
    if st.button("Get Advice"):
        if user_query_tab1:
            with st.spinner("Generating response..."):
                prompt = f"""
                Provide detailed nutrition advice for:
                Name: {st.session_state.user_info['name']}
                Age: {st.session_state.user_info['age']}
                Gender: {st.session_state.user_info['gender']}
                Weight: {st.session_state.user_info['weight']} kg
                Height: {st.session_state.user_info['height']} cm
                Goal: {st.session_state.user_info['goal']}
                Activity Level: {st.session_state.user_info['activity_level']}
                Preferred Diet: {st.session_state.user_info['diet']}
                Allergies: {', '.join(st.session_state.user_info['allergies']) if st.session_state.user_info['allergies'] else 'None'}
                Dietary Restrictions: {', '.join(st.session_state.user_info['restrictions']) if st.session_state.user_info['restrictions'] else 'None'}
                Meals per day: {st.session_state.user_info['meals_per_day']}
                Snacks per day: {st.session_state.user_info['snacks_per_day']}
                
                Question: {user_query_tab1}
                
                If the user's question implies meal ideas, please include simple recipe suggestions with ingredients and instructions.
                
                Respond in a friendly tone with practical recommendations.
                """
                
                try:
                    response = get_gemini_response(prompt)
                    st.session_state.last_response = response
                    
                    st.subheader("Nutrition Advice")
                    st.write(response)
                    
                    
                    # Save interaction
                    save_user_response(
                        st.session_state.user_info["name"],
                        st.session_state.user_info["age"],
                        st.session_state.user_info["goal"],
                        user_query_tab1,
                        response
                    )

                except Exception as e:
                    st.error(f"Failed to get AI response: {str(e)}")
        else:
            st.warning("Please enter a question")

#Voice Input Tab
with tab2:
    st.subheader("Speak Your Nutrition Question")
    if st.button("Start Voice Assistant"):
        with st.spinner("Listening..."):
            user_query = transcribe_microphone()
            
            if user_query and "Error" not in user_query:
                st.success(f"Detected: {user_query}")
                
                with st.spinner("Analyzing..."):
                    prompt = f"""
                    Provide detailed nutrition advice for:
                    Name: {st.session_state.user_info['name']}
                    Age: {st.session_state.user_info['age']}
                    Gender: {st.session_state.user_info['gender']}
                    Weight: {st.session_state.user_info['weight']} kg
                    Height: {st.session_state.user_info['height']} cm
                    Goal: {st.session_state.user_info['goal']}
                    Activity Level: {st.session_state.user_info['activity_level']}
                    Preferred Diet: {st.session_state.user_info['diet']}
                    Allergies: {', '.join(st.session_state.user_info['allergies']) if st.session_state.user_info['allergies'] else 'None'}
                    Dietary Restrictions: {', '.join(st.session_state.user_info['restrictions']) if st.session_state.user_info['restrictions'] else 'None'}
                    Meals per day: {st.session_state.user_info['meals_per_day']}
                    Snacks per day: {st.session_state.user_info['snacks_per_day']}
                    
                    Question: {user_query}
                    Respond in a friendly tone with practical recommendations.
                    """
                    
                    try:
                        response = get_gemini_response(prompt)
                        st.session_state.last_response = response
                        
                        st.subheader("Nutrition Advice")
                        st.write(response)
                        
                        
                        save_user_response(
                            st.session_state.user_info["name"],
                            st.session_state.user_info["age"],
                            st.session_state.user_info["goal"],
                            user_query,
                            response
                        )


                    except Exception as e:
                        st.error(f"Failed to get AI response: {str(e)}")
            else:
                st.warning("Could not transcribe audio")

#Image Analysis Tab
with tab3:
    st.subheader("Analyze Food Image")
    uploaded_image = st.file_uploader("Upload food image", type=["jpg", "jpeg", "png"])
    
    if uploaded_image and st.button("Analyze Food"):
        with st.spinner("Analyzing..."):
            st.image(uploaded_image, width=300)
            try:
                analysis = analyze_image_with_gemini(uploaded_image)
                if "sorry" not in analysis.lower():
                    st.subheader("Food Analysis")
                    st.write(analysis)
                else:
                    st.warning(analysis)
            except Exception as e:
                st.error(f"Image analysis failed: {str(e)}")

#Calculators Tab
with tab4:
    st.subheader("Health Calculators")

    #BMI Calculator
    st.markdown("#### Body Mass Index (BMI)")
    weight_bmi = st.session_state.user_info["weight"]
    height_bmi = st.session_state.user_info["height"]
    
    if st.button("Calculate BMI"):
        bmi_val, bmi_cat = calculate_bmi(weight_bmi, height_bmi)
        if bmi_val:
            st.success(f"Your BMI: {bmi_val:.2f}")
            st.info(f"Category: {bmi_cat}")
        else:
            st.error("Invalid height/weight")

    st.markdown("---")

    # Calorie Calculator
    st.markdown("#### Daily Calorie Needs (TDEE)")
    gend_cal = st.session_state.user_info["gender"]
    weight_cal = st.session_state.user_info["weight"]
    height_cal = st.session_state.user_info["height"] 
    age_cal = st.session_state.user_info["age"]
    activity_cal = st.session_state.user_info["activity_level"]

    if st.button("Calculate Calories"):
        bmr_val = calculate_bmr(gend_cal, weight_cal, height_cal, age_cal)
        if bmr_val:
            tdee_val = calculate_tdee(bmr_val, activity_cal)
            if tdee_val:
                st.success(f"BMR: {bmr_val:.0f} calories/day")
                st.info(f"TDEE ({activity_cal}): {tdee_val:.0f} calories/day")
                st.markdown("*Estimated daily calorie needs to maintain current weight*")
            else:
                st.error("Invalid activity level")
        else:
            st.error("Invalid inputs")

#Exercise Suggestions Tab
with tab5:
    st.subheader("Personalized Exercise Suggestions")
    
    if st.button("Get Suggestions"):
        with st.spinner("Generating..."):
            suggestions = get_exercise_suggestions(st.session_state.user_info["goal"], st.session_state.user_info)
            st.write(suggestions)
        
# Footer
st.markdown("---")
st.caption("© 2025 Smartest Nutrition AI Assistant | Surbhi Sharma")