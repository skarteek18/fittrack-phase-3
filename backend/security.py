

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime, date
from enum import Enum


# ==========================================
# COMMON CONFIGURATION
# ==========================================

class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ==========================================
# MODULE 13: NUTRITION & MEAL TRACKING
# ==========================================

class MealType(str, Enum):
    BREAKFAST = "Breakfast"
    LUNCH = "Lunch"
    DINNER = "Dinner"
    SNACKS = "Snacks"


class MealCreate(BaseModel):

    meal_type: MealType

    food_name: str = Field(
        ...,
        min_length=2,
        max_length=200
    )

    calories: float = Field(
        ...,
        ge=0
    )

    protein: float = Field(
        default=0,
        ge=0
    )

    carbs: float = Field(
        default=0,
        ge=0
    )

    fats: float = Field(
        default=0,
        ge=0
    )


class MealUpdate(BaseModel):

    meal_type: Optional[MealType] = None
    food_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=200
    )

    calories: Optional[float] = Field(
        default=None,
        ge=0
    )

    protein: Optional[float] = Field(
        default=None,
        ge=0
    )

    carbs: Optional[float] = Field(
        default=None,
        ge=0
    )

    fats: Optional[float] = Field(
        default=None,
        ge=0
    )


class MealResponse(BaseSchema):

    id: int
    user_id: int
    meal_type: MealType
    food_name: str
    calories: float
    protein: float
    carbs: float
    fats: float
    created_at: Optional[datetime] = None


class NutritionSummary(BaseModel):

    total_calories: float = 0
    total_protein: float = 0
    total_carbs: float = 0
    total_fats: float = 0

    total_meals: int = 0
    date: date


# ==========================================
# MODULE 14: WATER INTAKE TRACKER
# ==========================================

class WaterCreate(BaseModel):

    quantity: int = Field(
        ...,
        gt=0,
        le=10000
    )

    date: Optional[date] = None


class WaterResponse(BaseSchema):

    id: int
    user_id: int
    quantity: int
    date: date


class WaterGoalCreate(BaseModel):

    daily_goal: int = Field(
        default=2500,
        gt=0,
        le=10000
    )


class WaterSummary(BaseModel):

    total_consumed: int = 0
    daily_goal: int = 2500
    remaining: int = 2500
    progress_percentage: float = 0
    consumed_liters: float = 0
    date: date


# ==========================================
# MODULE 15: AI WORKOUT SUGGESTIONS
# ==========================================

class WorkoutSuggestionRequest(BaseModel):

    fitness_goal: Optional[str] = None

    fitness_level: Optional[str] = "Beginner"

    preferred_duration: int = Field(
        default=30,
        gt=0,
        le=300
    )


class RecommendedExercise(BaseModel):

    exercise_name: str

    description: str

    duration: int

    difficulty: str

    calories_estimate: float


class WorkoutRecommendationResponse(BaseModel):

    user_id: int

    fitness_goal: str

    recommendations: List[RecommendedExercise]

    message: str


# ==========================================
# MODULE 16: WORKOUT TIMER & LIVE TRACKING
# ==========================================

class WorkoutTimerStart(BaseModel):

    workout_name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    activity_type: str = Field(
        default="General"
    )


class WorkoutTimerStop(BaseModel):

    workout_id: int

    duration_seconds: int = Field(
        ...,
        gt=0
    )

    calories_burned: float = Field(
        default=0,
        ge=0
    )


class WorkoutTimerResponse(BaseModel):

    workout_id: int

    workout_name: str

    start_time: datetime

    end_time: Optional[datetime] = None

    duration_seconds: int = 0

    calories_burned: float = 0

    status: str


# ==========================================
# MODULE 17: THIRD-PARTY INTEGRATIONS
# ==========================================

class IntegrationCreate(BaseModel):

    provider: str = Field(
        ...,
        min_length=2,
        max_length=50
    )

    access_token: Optional[str] = None


class IntegrationResponse(BaseModel):

    provider: str

    connected: bool

    message: str


class ActivitySync(BaseModel):

    steps: int = Field(
        default=0,
        ge=0
    )

    calories_burned: float = Field(
        default=0,
        ge=0
    )

    active_minutes: int = Field(
        default=0,
        ge=0
    )

    sync_date: Optional[date] = None


# ==========================================
# MODULE 18: ADVANCED ANALYTICS
# ==========================================

class WeeklyAnalytics(BaseModel):

    total_workouts: int = 0

    total_duration: float = 0

    total_calories_burned: float = 0

    completed_goals: int = 0

    workout_consistency: float = 0


class MonthlyAnalytics(BaseModel):

    total_workouts: int = 0

    total_duration: float = 0

    total_calories_burned: float = 0

    goal_completion_rate: float = 0

    average_workouts_per_week: float = 0


class AnalyticsResponse(BaseModel):

    user_id: int

    weekly: WeeklyAnalytics

    monthly: MonthlyAnalytics

    insights: List[str] = []


# ==========================================
# MODULE 19: IN-APP REMINDERS & ALERTS
# ==========================================

class ReminderType(str, Enum):

    WORKOUT = "Workout"

    MEAL = "Meal"

    WATER = "Water"


class ReminderCreate(BaseModel):

    reminder_type: ReminderType

    title: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    message: Optional[str] = None

    reminder_time: datetime

    is_active: bool = True


class ReminderUpdate(BaseModel):

    title: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    message: Optional[str] = None

    reminder_time: Optional[datetime] = None

    is_active: Optional[bool] = None


class ReminderResponse(BaseSchema):

    id: int

    user_id: int

    reminder_type: ReminderType

    title: str

    message: Optional[str] = None

    reminder_time: datetime

    is_active: bool


# ==========================================
# COMMON API RESPONSE
# ==========================================

class SuccessResponse(BaseModel):

    success: bool = True

    message: str

    data: Optional[dict] = None


class ErrorResponse(BaseModel):

    success: bool = False

    message: str
