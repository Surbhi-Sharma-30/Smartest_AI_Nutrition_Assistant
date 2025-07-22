
# Smartest Nutrition AI Assistant

A Streamlit-based intelligent assistant that provides personalized nutrition advice, calculates BMI and calorie needs, suggests exercises, and supports voice & image input — all powered by AI.

![Banner](https://via.placeholder.com/1000x300?text=Smartest+Nutrition+AI+Assistant)

---

## Features

- **AI Chat**: Get personalized nutrition answers based on your profile.
- **Voice Assistant**: Ask your questions through voice.
- **Image Analysis**: Upload food images and receive nutrition insights.
- **Calculators**: Compute your BMI, BMR, and TDEE in one click.
- **Exercise Suggestions**: Receive goal-based fitness recommendations.
- **Beautiful UI**: Styled with custom background and CSS for a modern, smooth experience.

---

## Technologies Used

- [Streamlit](https://streamlit.io/)
- [Python](https://www.python.org/)
- [Google Gemini API or OpenAI](https://ai.google.dev/) *(for chat/image analysis)*
- [gTTS](https://pypi.org/project/gTTS/)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [dotenv](https://pypi.org/project/python-dotenv/)

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/nutrition-ai-assistant.git
cd nutrition-ai-assistant
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

---

## Run the App Locally

```bash
streamlit run nutrition_assistant.py
```

Open in your browser at `http://localhost:8501`.

---

## Deploy on Streamlit Cloud

1. Push your project to GitHub.
2. Go to [Streamlit Cloud](https://streamlit.io/cloud).
3. Connect your GitHub repo.
4. Set `nutrition_assistant.py` as the entry point.
5. Add a `.streamlit/secrets.toml` file to store API keys securely:
```toml
API_KEY = "your-gemini-or-openai-api-key"
```

---

## Project Structure

```
nutrition-ai-assistant/
├── bmi_calculator.py
├── calorie_calculator.py
├── csv_handler.py
├── exercise_suggestions.py
├── gemini_api_handler.py
├── voice_to_text.py
├── nutrition_assistant.py
├── requirements.txt
├── .env
├── NutriAI.jpg
└── README.md
```

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Author

**Surbhi Sharma**   
LinkedIn: (https://www.linkedin.com/in/surbhisharma3010?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3BYQbLFpSxSv%2BS2DbTOtSQMg%3D%3D)

---

> Made using Streamlit to promote smart & healthy living.
