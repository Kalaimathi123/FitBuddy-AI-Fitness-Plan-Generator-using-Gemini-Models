import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None

MODEL = "gemini-2.0-flash-lite"

def generate_workout_gemini(age, weight, goal, intensity):
    if not client:
        return f"Sample Workout Plan for {goal} - {intensity}:\n- Warmup 10 min\n- Squats 3 sets\n- Plank 1 min\n- Cool down"
    try:
        prompt = f"Create a workout plan for age {age}, weight {weight}kg, goal {goal}, intensity {intensity}. Give warmup, exercises with sets/reps, cool down in simple format."
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Sample Workout Plan for {goal} - {intensity}:\n- Warmup 10 min\n- Error was: {e}"

def generate_nutrition_tip_with_flash(goal):
    if not client:
        return f"Eat protein rich food for {goal}"
    try:
        prompt = f"Give 1 short nutrition tip for fitness goal {goal}"
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Eat healthy for {goal}"