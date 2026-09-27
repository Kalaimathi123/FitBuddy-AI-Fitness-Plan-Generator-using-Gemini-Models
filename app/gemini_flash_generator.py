import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def _call_gemini(prompt: str):
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )
    return response.text

def generate_workout_gemini(age, weight, goal, intensity):
    prompt = f"""
    Create a full 7-day fitness plan with workout + diet + warmup + cooldown
    User Details: Age {age}, Weight {weight}, Goal {goal}, Intensity {intensity}
    For each day MUST include: Warm-up, Exercise | Sets | Reps | Rest, Cool-down, Food Diet Morning/Afternoon/Night
    """
    return _call_gemini(prompt)

def generate_nutrition_tip_with_flash(age, weight, goal, intensity):
    prompt = f"Give nutrition tip for Age {age}, Weight {weight}, Goal {goal}, Intensity {intensity}"
    return _call_gemini(prompt)
