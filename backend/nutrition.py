

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date

from Database import get_db
from Models import Meal
from Schemas import MealCreate, MealUpdate, MealResponse, NutritionSummary
from Security import get_current_user

router = APIRouter(tags=["Nutrition"])


# -----------------------------
# Add Meal
# -----------------------------

@router.post("/meals", response_model=MealResponse,
             status_code=status.HTTP_201_CREATED)
def add_meal(
    meal_data: MealCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    new_meal = Meal(
        user_id=current_user.id,
        meal_type=meal_data.meal_type,
        food_name=meal_data.food_name,
        calories=meal_data.calories,
        protein=meal_data.protein,
        carbs=meal_data.carbs,
        fats=meal_data.fats
    )

    db.add(new_meal)
    db.commit()
    db.refresh(new_meal)

    return new_meal


# -----------------------------
# Get All Meals
# -----------------------------

@router.get("/meals", response_model=list[MealResponse])
def get_meals(
    meal_date: date = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    query = db.query(Meal).filter(
        Meal.user_id == current_user.id
    )

    if meal_date:
        query = query.filter(
            func.date(Meal.created_at) == meal_date
        )

    return query.order_by(Meal.created_at.desc()).all()


# -----------------------------
# Get Meal By ID
# -----------------------------

@router.get("/meals/{meal_id}", response_model=MealResponse)
def get_meal(
    meal_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    meal = db.query(Meal).filter(
        Meal.id == meal_id,
        Meal.user_id == current_user.id
    ).first()

    if not meal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal not found"
        )

    return meal


# -----------------------------
# Update Meal
# -----------------------------

@router.put("/meals/{meal_id}", response_model=MealResponse)
def update_meal(
    meal_id: int,
    meal_data: MealUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    meal = db.query(Meal).filter(
        Meal.id == meal_id,
        Meal.user_id == current_user.id
    ).first()

    if not meal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal not found"
        )

    update_data = meal_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(meal, key, value)

    db.commit()
    db.refresh(meal)

    return meal


# -----------------------------
# Delete Meal
# -----------------------------

@router.delete("/meals/{meal_id}")
def delete_meal(
    meal_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    meal = db.query(Meal).filter(
        Meal.id == meal_id,
        Meal.user_id == current_user.id
    ).first()

    if not meal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal not found"
        )

    db.delete(meal)
    db.commit()

    return {"message": "Meal deleted successfully"}


# -----------------------------
# Daily Nutrition Summary
# -----------------------------

@router.get("/summary/daily", response_model=NutritionSummary)
def get_daily_nutrition(
    meal_date: date = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    selected_date = meal_date or date.today()

    summary = db.query(
        func.coalesce(func.sum(Meal.calories), 0).label("total_calories"),
        func.coalesce(func.sum(Meal.protein), 0).label("total_protein"),
        func.coalesce(func.sum(Meal.carbs), 0).label("total_carbs"),
        func.coalesce(func.sum(Meal.fats), 0).label("total_fats")
    ).filter(
        Meal.user_id == current_user.id,
        func.date(Meal.created_at) == selected_date
    ).first()

    return {
        "date": selected_date,
        "total_calories": summary.total_calories,
        "total_protein": summary.total_protein,
        "total_carbs": summary.total_carbs,
        "total_fats": summary.total_fats
    }


# -----------------------------
# Nutrition Summary By Meal Type
# -----------------------------

@router.get("/summary/by-meal")
def get_nutrition_by_meal(
    meal_date: date = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    selected_date = meal_date or date.today()

    results = db.query(
        Meal.meal_type,
        func.sum(Meal.calories).label("calories"),
        func.sum(Meal.protein).label("protein"),
        func.sum(Meal.carbs).label("carbs"),
        func.sum(Meal.fats).label("fats")
    ).filter(
        Meal.user_id == current_user.id,
        func.date(Meal.created_at) == selected_date
    ).group_by(Meal.meal_type).all()

    return [
        {
            "meal_type": row.meal_type,
            "calories": row.calories or 0,
            "protein": row.protein or 0,
            "carbs": row.carbs or 0,
            "fats": row.fats or 0
        }
        for row in results
    ]
