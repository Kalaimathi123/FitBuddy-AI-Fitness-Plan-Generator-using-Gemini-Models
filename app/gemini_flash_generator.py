from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def _call_gemini(prompt: str):
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )
    return response.text

def generate_workout_gemini(age, weight, goal, intensity):
    prompt = f"Create a 7-day fitness plan for Age {age}, Weight {weight}, Goal {goal}, Intensity {intensity}. Include Warm-up, Workout, Diet."
    return _call_gemini(prompt)

def generate_nutrition_tip_with_flash(goal):
    prompt = f"Give a short nutrition tip for fitness goal: {goal}"
    return _call_gemini(prompt)
