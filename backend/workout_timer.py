

from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from Database import get_db
from Models import Workout
from Schemas import WorkoutTimerStart, WorkoutTimerStop, WorkoutTimerResponse
from Security import get_current_user

router = APIRouter(tags=["Workout Timer"])


# -----------------------------
# Start Workout Timer
# -----------------------------

@router.post(
    "/start",
    response_model=WorkoutTimerResponse,
    status_code=status.HTTP_201_CREATED
)
def start_workout(
    workout_data: WorkoutTimerStart,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Check whether the user already has an active session.
    active_workout = db.query(Workout).filter(
        Workout.user_id == current_user.id,
        Workout.end_time.is_(None)
    ).first()

    if active_workout:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have an active workout session"
        )

    workout = Workout(
        user_id=current_user.id,
        workout_type=workout_data.workout_type,
        duration=0,
        calories_burned=0,
        created_at=datetime.now(timezone.utc),
        start_time=datetime.now(timezone.utc),
        end_time=None
    )

    db.add(workout)
    db.commit()
    db.refresh(workout)

    return {
        "workout_id": workout.id,
        "workout_type": workout.workout_type,
        "start_time": workout.start_time,
        "end_time": None,
        "duration": 0,
        "calories_burned": 0,
        "status": "active"
    }


# -----------------------------
# Stop Workout Timer
# -----------------------------

@router.post(
    "/stop/{workout_id}",
    response_model=WorkoutTimerResponse
)
def stop_workout(
    workout_id: int,
    workout_data: WorkoutTimerStop,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    workout = db.query(Workout).filter(
        Workout.id == workout_id,
        Workout.user_id == current_user.id
    ).first()

    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout session not found"
        )

    if workout.end_time is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Workout session has already been stopped"
        )

    end_time = datetime.now(timezone.utc)

    start_time = workout.start_time

    if start_time.tzinfo is None:
        start_time = start_time.replace(tzinfo=timezone.utc)

    elapsed_seconds = max(
        0,
        int((end_time - start_time).total_seconds())
    )

    duration_minutes = max(
        1,
        round(elapsed_seconds / 60)
    )

    # Estimate calories using workout type and duration.
    calorie_rates = {
        "running": 10,
        "cycling": 8,
        "walking": 4,
        "weight training": 6,
        "yoga": 3,
        "cardio": 8
    }

    workout_type = workout.workout_type.lower()

    calories_per_minute = calorie_rates.get(
        workout_type,
        5
    )

    calories_burned = round(
        duration_minutes * calories_per_minute
    )

    workout.end_time = end_time
    workout.duration = duration_minutes
    workout.calories_burned = calories_burned

    db.commit()
    db.refresh(workout)

    return {
        "workout_id": workout.id,
        "workout_type": workout.workout_type,
        "start_time": workout.start_time,
        "end_time": workout.end_time,
        "duration": workout.duration,
        "calories_burned": workout.calories_burned,
        "status": "completed"
    }


# -----------------------------
# Get Active Workout
# -----------------------------

@router.get("/active")
def get_active_workout(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    workout = db.query(Workout).filter(
        Workout.user_id == current_user.id,
        Workout.end_time.is_(None)
    ).first()

    if not workout:
        return {
            "active": False,
            "message": "No active workout session"
        }

    start_time = workout.start_time

    if start_time.tzinfo is None:
        start_time = start_time.replace(tzinfo=timezone.utc)

    elapsed_seconds = max(
        0,
        int((datetime.now(timezone.utc) - start_time).total_seconds())
    )

    return {
        "active": True,
        "workout_id": workout.id,
        "workout_type": workout.workout_type,
        "start_time": workout.start_time,
        "elapsed_seconds": elapsed_seconds,
        "elapsed_minutes": elapsed_seconds // 60
    }


# -----------------------------
# Workout Session History
# -----------------------------

@router.get("/history")
def get_workout_timer_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    workouts = db.query(Workout).filter(
        Workout.user_id == current_user.id,
        Workout.end_time.isnot(None)
    ).order_by(
        Workout.start_time.desc()
    ).all()

    return {
        "total_sessions": len(workouts),
        "total_duration": sum(
            workout.duration or 0 for workout in workouts
        ),
        "total_calories": sum(
            workout.calories_burned or 0 for workout in workouts
        ),
        "workouts": workouts
    }
