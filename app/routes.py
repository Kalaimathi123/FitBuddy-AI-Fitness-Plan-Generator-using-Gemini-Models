import traceback
import os
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.gemini_flash_generator import generate_workout_gemini, generate_nutrition_tip_with_flash

router = APIRouter()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "app", "templates")
templates = Jinja2Templates(directory=TEMPLATE_DIR)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"request": request})

@router.post('/generate-workout', response_class=HTMLResponse)
def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: int = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        workout_plan = generate_workout_gemini(age, weight, goal, intensity)
        nutrition_tip = generate_nutrition_tip_with_flash(age, weight, goal, intensity)

        # Check if user exists, if yes update
        existing = db.query(User).filter(User.user_id == user_id).first()
        if existing:
            existing.username = username
            existing.age = age
            existing.weight = weight
            existing.goal = goal
            existing.intensity = intensity
            existing.workout_plan = workout_plan
            existing.nutrition_tip = nutrition_tip
            db.commit()
            db.refresh(existing)
        else:
            new_user = User(
                user_id=user_id,
                username=username,
                age=age,
                weight=weight,
                goal=goal,
                intensity=intensity,
                workout_plan=workout_plan,
                nutrition_tip=nutrition_tip
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

        return templates.TemplateResponse(request, "result.html", {
            "request": request,
            "username": username,
            "user_id": user_id,
            "age": age,
            "weight": weight,
            "goal": goal,
            "intensity": intensity,
            "workout_plan": workout_plan,
            "nutrition_tip": nutrition_tip
        })
    except Exception as e:
        traceback.print_exc()
        return HTMLResponse(f"<h1>Error</h1><pre>{str(e)}\n{traceback.format_exc()}</pre>", status_code=500)

@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(request: Request, user_id: str = Form(...), feedback: str = Form(...), db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            return HTMLResponse(f"<h1>User {user_id} not found</h1><a href='/'>Go back</a>", status_code=404)
        
        # Regenerate based on feedback
        new_prompt_goal = f"{user.goal} with feedback: {feedback}"
        new_workout = generate_workout_gemini(user.age, user.weight, new_prompt_goal, user.intensity)
        
        user.feedback = feedback
        user.workout_plan = new_workout
        db.commit()

        return templates.TemplateResponse(request, "result.html", {
            "request": request,
            "username": user.username,
            "user_id": user.user_id,
            "age": user.age,
            "weight": user.weight,
            "goal": user.goal,
            "intensity": user.intensity,
            "workout_plan": new_workout,
            "nutrition_tip": user.nutrition_tip,
            "updated": True
        })
    except Exception as e:
        traceback.print_exc()
        return HTMLResponse(f"<h1>Error</h1><pre>{str(e)}\n{traceback.format_exc()}</pre>", status_code=500)

@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    html = "<h1>All Users</h1><a href='/'>Back</a><ul>"
    for u in users:
        html += f"<li>{u.user_id} - {u.username} - {u.goal} - {u.intensity}</li>"
    html += "</ul>"
    return HTMLResponse(html)