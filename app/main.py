import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.database import init_db
from app.routes import router

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if os.path.exists(os.path.join(BASE_DIR, "static")):
    STATIC_DIR = os.path.join(BASE_DIR, "static")
else:
    STATIC_DIR = os.path.join(BASE_DIR, "app", "static")

os.makedirs(STATIC_DIR, exist_ok=True)

app = FastAPI(title="FitBuddy - AI Fitness Plan Generator")

init_db()

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.include_router(router)

# ITHA ADD PANNEN DA - WHITE SCREEN FIX
@app.get("/check")
async def check():
    return {"status": "FitBuddy Working!"}