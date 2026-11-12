

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Database import engine, Base

from Auth import router as auth_router
from Nutrition import router as nutrition_router
from Water_Tracking import router as water_router
from AI_Recommendations import router as recommendations_router
from Workout_Timer import router as timer_router
from Integrations import router as integrations_router
from Analytics import router as analytics_router
from Reminders import router as reminders_router


# Initialize Database
Base.metadata.create_all(bind=engine)


# Initialize FastAPI Application
app = FastAPI(
    title="FitTrack API",
    description="Fitness and Workout Management Platform - Phase 3",
    version="3.0.0"
)


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register Authentication Router
app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)


# Module 13: Nutrition & Meal Tracking
app.include_router(
    nutrition_router,
    prefix="/nutrition",
    tags=["Nutrition & Meal Tracking"]
)


# Module 14: Water Intake Tracker
app.include_router(
    water_router,
    prefix="/water",
    tags=["Water Intake Tracking"]
)


# Module 15: AI Workout Suggestions
app.include_router(
    recommendations_router,
    prefix="/recommendations",
    tags=["AI Workout Recommendations"]
)


# Module 16: Workout Timer & Live Tracking
app.include_router(
    timer_router,
    prefix="/workout-timer",
    tags=["Workout Timer & Live Tracking"]
)


# Module 17: Third-Party Integration
app.include_router(
    integrations_router,
    prefix="/integrations",
    tags=["Third-Party Integrations"]
)


# Module 18: Advanced Analytics Dashboard
app.include_router(
    analytics_router,
    prefix="/analytics",
    tags=["Advanced Analytics"]
)


# Module 19: In-App Reminders & Alerts
app.include_router(
    reminders_router,
    prefix="/reminders",
    tags=["Reminders & Alerts"]
)


# Root Endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to FitTrack API",
        "project": "FitTrack Fitness Management Platform",
        "phase": "Phase 3",
        "version": "3.0.0",
        "status": "Running"
    }


# Health Check Endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "FitTrack",
        "phase": "Phase 3"
    }


# API Information
@app.get("/api-info")
def api_info():
    return {
        "project": "FitTrack",
        "phase": "Smart Features & Advanced Analytics",
        "modules": [
            "Nutrition & Meal Tracking",
            "Water Intake Tracker",
            "AI Workout Suggestions",
            "Workout Timer & Live Tracking",
            "Third-Party Integration",
            "Advanced Analytics Dashboard",
            "In-App Reminders & Alerts"
        ],
        "documentation": "/docs"
    }


# Application Startup
@app.on_event("startup")
def startup_event():
    print("====================================")
    print("       FITTRACK API STARTED")
    print("====================================")
    print("Phase: 3")
    print("Version: 3.0.0")
    print("Status: Running")
    print("API Docs: http://127.0.0.1:8000/docs")
    print("====================================")


# Application Shutdown
@app.on_event("shutdown")
def shutdown_event():
    print("FitTrack API shutting down...")
