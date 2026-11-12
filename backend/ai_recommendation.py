from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from Database import get_db
from Models import Workout, Goal, Streak
from Schemas import (
    WorkoutSuggestionRequest,
    RecommendedExercise,
    WorkoutRecommendationResponse
)
from Security import get_current_user

router = APIRouter(tags=["AI Workout Recommendations"])


# -----------------------------
# Exercise Recommendation Data
# -----------------------------

EXERCISE_LIBRARY = {
    "weight_loss": [
        {
            "name": "Running",
            "category": "Cardio",
            "duration": 20,
            "intensity": "High",
            "description": "Improves cardiovascular fitness and burns calories."
        },
        {
            "name": "Jumping Jacks",
            "category": "Cardio",
            "duration": 10,
            "intensity": "Medium",
            "description": "A full-body cardiovascular exercise."
        },
        {
            "name": "Cycling",
            "category": "Cardio",
            "duration": 25,
            "intensity": "Medium",
            "description": "Supports calorie burning and endurance."
        }
    ],
    "muscle_gain": [
        {
            "name": "Push-ups",
            "category": "Strength",
            "duration": 15,
            "intensity": "Medium",
            "description": "Strengthens the chest, shoulders and triceps."
        },
        {
            "name": "Squats",
            "category": "Strength",
            "duration": 20,
            "intensity": "High",
            "description": "Builds lower-body strength."
        },
        {
            "name": "Dumbbell Rows",
            "category": "Strength",
            "duration": 15,
            "intensity": "Medium",
            "description": "Targets the back and arm muscles."
        }
    ],
    "fitness": [
        {
            "name": "Brisk Walking",
            "category": "Cardio",
            "duration": 20,
            "intensity": "Low",
            "description": "Improves general cardiovascular health."
        },
        {
            "name": "Plank",
            "category": "Core",
            "duration": 5,
            "intensity": "Medium",
            "description": "Develops core stability."
        },
        {
            "name": "Yoga",
            "category": "Flexibility",
            "duration": 20,
            "intensity": "Low",
            "description": "Improves flexibility and balance."
        }
    ]
}


# -----------------------------
# Get Workout History
# -----------------------------

@router.get("/history")
def get_workout_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    workouts = db.query(Workout).filter(
        Workout.user_id == current_user.id
    ).order_by(Workout.id.desc()).limit(20).all()

    return {
        "total_workouts": len(workouts),
        "workouts": workouts
    }


# -----------------------------
# Generate Recommendations
# -----------------------------

@router.post(
    "/generate",
    response_model=WorkoutRecommendationResponse
)
def generate_recommendations(
    request: WorkoutSuggestionRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    goal_name = (
        request.goal or "fitness"
    ).lower().replace(" ", "_")

    if goal_name not in EXERCISE_LIBRARY:
        goal_name = "fitness"

    # Analyze recent workout history.
    start_date = datetime.utcnow() - timedelta(days=7)

    recent_workouts = db.query(Workout).filter(
        Workout.user_id == current_user.id,
        Workout.created_at >= start_date
    ).all()

    weekly_count = len(recent_workouts)

    # Select exercise recommendations.
    selected_exercises = EXERCISE_LIBRARY[goal_name]

    # Adjust intensity according to workout consistency.
    if weekly_count == 0:
        selected_exercises = [
            exercise for exercise in selected_exercises
            if exercise["intensity"] != "High"
        ]

    elif weekly_count >= 5:
        selected_exercises = selected_exercises[:3]

    recommendations = [
        RecommendedExercise(
            name=exercise["name"],
            category=exercise["category"],
            duration=exercise["duration"],
            intensity=exercise["intensity"],
            description=exercise["description"]
        )
        for exercise in selected_exercises
    ]

    # Generate personalized insight.
    if weekly_count == 0:
        insight = (
            "You have not recorded a workout this week. "
            "Start with light exercises and build consistency."
        )
    elif weekly_count < 3:
        insight = (
            "Good start! Try maintaining a regular workout routine "
            "throughout the week."
        )
    else:
        insight = (
            "Great consistency! Continue balancing workout intensity "
            "with sufficient recovery."
        )

    return WorkoutRecommendationResponse(
        goal=goal_name,
        weekly_workouts=weekly_count,
        recommendations=recommendations,
        insight=insight
    )


# -----------------------------
# Get Today's Recommendation
# -----------------------------

@router.get("/today")
def get_today_recommendation(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    start_date = datetime.utcnow() - timedelta(days=7)

    workout_count = db.query(func.count(Workout.id)).filter(
        Workout.user_id == current_user.id,
        Workout.created_at >= start_date
    ).scalar() or 0

    if workout_count == 0:
        message = "Start with a light 15-minute walk today."
    elif workout_count < 3:
        message = "Try a 20-minute cardio or strength session today."
    else:
        message = "Maintain your routine and include recovery exercises."

    return {
        "weekly_workouts": workout_count,
        "recommendation": message
    }


# -----------------------------
# Get Available Workout Goals
# -----------------------------

@router.get("/goals")
def get_recommendation_goals():
    return {
        "available_goals": [
            "weight_loss",
            "muscle_gain",
            "fitness"
        ]
    }
