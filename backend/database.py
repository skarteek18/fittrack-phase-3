

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

# Database Configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./fittrack.db"
)

# SQLite Configuration
connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# Create Database Engine
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True
)

# Create Session Factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base Class for SQLAlchemy Models
Base = declarative_base()


# Database Dependency
def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# Initialize Database
def init_db():
    Base.metadata.create_all(bind=engine)


# Database Connection Test
def check_database_connection():
    try:
        from sqlalchemy import text

        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return True

    except Exception as error:
        print(f"Database connection failed: {error}")
        return False


# Database Status
def database_status():
    if check_database_connection():
        return {
            "database": "Connected",
            "status": "Healthy"
        }

    return {
        "database": "Disconnected",
        "status": "Unhealthy"
    }
