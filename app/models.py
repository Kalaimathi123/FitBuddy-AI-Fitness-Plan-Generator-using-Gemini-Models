from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    username = Column(String, index=True)
    age = Column(Integer)
    weight = Column(Integer)
    goal = Column(String)
    intensity = Column(String)
    workout_plan = Column(String)
    nutrition_tip = Column(String)
    feedback = Column(String, nullable=True)