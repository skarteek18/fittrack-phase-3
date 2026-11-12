

from datetime import date, datetime, timedelta
from calendar import monthrange

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from Database import get_db
from Models import Workout, Goal, Progress
from Security import get_current_user

router = APIRouter(tags=["Advanced Analytics"])


# -----------------------------
# Weekly Analytics
# -----------------------------

@router.get("/weekly")
def get_weekly_analytics(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    start_datetime = datetime.combine(
        week_start, datetime.min.time()
    )

    end_datetime = datetime.combine(
        week_end + timedelta(days=1), datetime.min.time()
    )

    workouts = db.query(Workout).filter(
        Workout.user_id == current_user.id,
        Workout.created_at >= start_datetime,
        Workout.created_at < end_datetime
    ).all()

    total_workouts = len(workouts)

    total_duration = sum(
        workout.duration or 0 for workout in workouts
    )

    total_calories = sum(
        workout.calories_burned or 0 for workout in workouts
    )

    daily_data = []

    for day_offset in range(7):
        current_date = week_start + timedelta(days=day_offset)

        daily_workouts = [
            workout for workout in workouts
            if workout.created_at.date() == current_date
        ]

        daily_data.append({
            "date": current_date,
            "workouts": len(daily_workouts),
            "duration": sum(
                workout.duration or 0
                for workout in daily_workouts
            ),
            "calories": sum(
                workout.calories_burned or 0
                for workout in daily_workouts
            )
        })

    return {
        "period": "weekly",
        "week_start": week_start,
        "week_end": week_end,
        "total_workouts": total_workouts,
        "total_duration": total_duration,
        "total_calories": total_calories,
        "average_duration": round(
            total_duration / total_workouts, 2
        ) if total_workouts else 0,
        "daily_data": daily_data
    }


# -----------------------------
# Monthly Analytics
# -----------------------------

@router.get("/monthly")
def get_monthly_analytics(
    year: int = None,
    month: int = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    today = date.today()

    selected_year = year or today.year
    selected_month = month or today.month

    if selected_month < 1 or selected_month > 12:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=400,
            detail="Month must be between 1 and 12"
        )

    if selected_year < 2000 or selected_year > today.year + 1:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=400,
            detail="Invalid year"
        )

    start_date = date(selected_year, selected_month, 1)

    last_day = monthrange(
        selected_year, selected_month
    )[1]

    end_date = date(
        selected_year,
        selected_month,
        last_day
    )

    start_datetime = datetime.combine(
        start_date, datetime.min.time()
    )

    end_datetime = datetime.combine(
        end_date + timedelta(days=1), datetime.min.time()
    )

    workouts = db.query(Workout).filter(
        Workout.user_id == current_user.id,
        Workout.created_at >= start_datetime,
        Workout.created_at < end_datetime
    ).all()

    total_workouts = len(workouts)

    total_duration = sum(
        workout.duration or 0 for workout in workouts
    )

    total_calories = sum(
        workout.calories_burned or 0 for workout in workouts
    )

    return {
        "period": "monthly",
        "year": selected_year,
        "month": selected_month,
        "total_workouts": total_workouts,
        "total_duration": total_duration,
        "total_calories": total_calories,
        "average_duration": round(
            total_duration / total_workouts, 2
        ) if total_workouts else 0
    }


# -----------------------------
# Goal Completion Analytics
# -----------------------------

@router.get("/goals")
def get_goal_analytics(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    goals = db.query(Goal).filter(
        Goal.user_id == current_user.id
    ).all()

    total_goals = len(goals)

    completed_goals = sum(
        1 for goal in goals
        if getattr(goal, "is_completed", False)
    )

    pending_goals = total_goals - completed_goals

    completion_percentage = (
        round((completed_goals / total_goals) * 100, 2)
        if total_goals else 0
    )

    return {
        "total_goals": total_goals,
        "completed_goals": completed_goals,
        "pending_goals": pending_goals,
        "completion_percentage": completion_percentage
    }


# -----------------------------
# Workout Consistency Analytics
# -----------------------------

@router.get("/consistency")
def get_workout_consistency(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    today = date.today()
    start_date = today - timedelta(days=29)

    start_datetime = datetime.combine(
        start_date, datetime.min.time()
    )

    workouts = db.query(Workout).filter(
        Workout.user_id == current_user.id,
        Workout.created_at >= start_datetime
    ).all()

    active_days = len({
        workout.created_at.date()
        for workout in workouts
    })

    consistency_percentage = round(
        (active_days / 30) * 100, 2
    )

    return {
        "period": "last_30_days",
        "active_days": active_days,
        "inactive_days": 30 - active_days,
        "consistency_percentage": consistency_percentage,
        "total_workouts": len(workouts)
    }


# -----------------------------
# Fitness Insights
# -----------------------------

@router.get("/insights")
def get_fitness_insights(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    today = date.today()
    start_date = today - timedelta(days=6)

    start_datetime = datetime.combine(
        start_date, datetime.min.time()
    )

    workouts = db.query(Workout).filter(
        Workout.user_id == current_user.id,
        Workout.created_at >= start_datetime
    ).all()

    workout_count = len(workouts)

    total_calories = sum(
        workout.calories_burned or 0
        for workout in workouts
    )

    total_duration = sum(
        workout.duration or 0
        for workout in workouts
    )

    insights = []

    if workout_count == 0:
        insights.append(
            "Start with a light workout to build consistency."
        )
    elif workout_count >= 5:
        insights.append(
            "Excellent consistency! Keep balancing exercise and recovery."
        )
    else:
        insights.append(
            "Good progress! Try maintaining a regular workout schedule."
        )

    if total_duration >= 150:
        insights.append(
            "Great job reaching at least 150 workout minutes this week."
        )
    else:
        insights.append(
            "Try gradually increasing your weekly workout duration."
        )

    if total_calories > 0:
        insights.append(
            f"You burned approximately {total_calories} calories this week."
        )

    return {
        "weekly_workouts": workout_count,
        "weekly_duration": total_duration,
        "weekly_calories": total_calories,
        "insights": insights
    }
