

from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from Database import get_db
from Models import WaterTracking
from Schemas import WaterCreate, WaterResponse, WaterGoalCreate, WaterSummary
from Security import get_current_user
from Config import settings

router = APIRouter(tags=["Water Tracking"])


# Store daily goals temporarily.
# For permanent storage, create a WaterGoal model in Models.py.
water_goals = {}


# -----------------------------
# Log Water Intake
# -----------------------------

@router.post(
    "/log",
    response_model=WaterResponse,
    status_code=status.HTTP_201_CREATED
)
def log_water_intake(
    water_data: WaterCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    water_record = WaterTracking(
        user_id=current_user.id,
        quantity=water_data.quantity,
        date=water_data.date or date.today()
    )

    db.add(water_record)
    db.commit()
    db.refresh(water_record)

    return water_record


# -----------------------------
# Get Water Intake History
# -----------------------------

@router.get("/history", response_model=list[WaterResponse])
def get_water_history(
    water_date: date = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    query = db.query(WaterTracking).filter(
        WaterTracking.user_id == current_user.id
    )

    if water_date:
        query = query.filter(
            WaterTracking.date == water_date
        )

    return query.order_by(
        WaterTracking.date.desc(),
        WaterTracking.id.desc()
    ).all()


# -----------------------------
# Get Daily Water Summary
# -----------------------------

@router.get("/summary", response_model=WaterSummary)
def get_water_summary(
    water_date: date = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    selected_date = water_date or date.today()

    total_intake = db.query(
        func.coalesce(func.sum(WaterTracking.quantity), 0)
    ).filter(
        WaterTracking.user_id == current_user.id,
        WaterTracking.date == selected_date
    ).scalar()

    daily_goal = water_goals.get(
        current_user.id,
        settings.DEFAULT_WATER_GOAL
    )

    percentage = min(
        round((total_intake / daily_goal) * 100, 2),
        100
    ) if daily_goal > 0 else 0

    return {
        "date": selected_date,
        "total_intake": total_intake,
        "daily_goal": daily_goal,
        "remaining": max(daily_goal - total_intake, 0),
        "completion_percentage": percentage,
        "goal_completed": total_intake >= daily_goal
    }


# -----------------------------
# Set Daily Water Goal
# -----------------------------

@router.post("/goal")
def set_water_goal(
    goal_data: WaterGoalCreate,
    current_user=Depends(get_current_user)
):
    if goal_data.daily_goal <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Daily water goal must be greater than zero"
        )

    water_goals[current_user.id] = goal_data.daily_goal

    return {
        "message": "Daily water goal updated successfully",
        "daily_goal": goal_data.daily_goal
    }


# -----------------------------
# Delete Water Record
# -----------------------------

@router.delete("/{record_id}")
def delete_water_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    record = db.query(WaterTracking).filter(
        WaterTracking.id == record_id,
        WaterTracking.user_id == current_user.id
    ).first()

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Water intake record not found"
        )

    db.delete(record)
    db.commit()

    return {
        "message": "Water intake record deleted successfully"
    }
