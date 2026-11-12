

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from Database import get_db
from Models import Reminder
from Schemas import ReminderCreate, ReminderUpdate, ReminderResponse
from Security import get_current_user

router = APIRouter(tags=["Reminders"])


# -----------------------------
# Create Reminder
# -----------------------------

@router.post(
    "/",
    response_model=ReminderResponse,
    status_code=status.HTTP_201_CREATED
)
def create_reminder(
    reminder_data: ReminderCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    new_reminder = Reminder(
        user_id=current_user.id,
        title=reminder_data.title,
        description=reminder_data.description,
        reminder_type=reminder_data.reminder_type,
        reminder_time=reminder_data.reminder_time,
        is_enabled=reminder_data.is_enabled
    )

    db.add(new_reminder)
    db.commit()
    db.refresh(new_reminder)

    return new_reminder


# -----------------------------
# Get All Reminders
# -----------------------------

@router.get("/", response_model=list[ReminderResponse])
def get_reminders(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Reminder).filter(
        Reminder.user_id == current_user.id
    ).order_by(
        Reminder.reminder_time.asc()
    ).all()


# -----------------------------
# Get Reminder By ID
# -----------------------------

@router.get("/{reminder_id}", response_model=ReminderResponse)
def get_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.user_id == current_user.id
    ).first()

    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found"
        )

    return reminder


# -----------------------------
# Update Reminder
# -----------------------------

@router.put("/{reminder_id}", response_model=ReminderResponse)
def update_reminder(
    reminder_id: int,
    reminder_data: ReminderUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.user_id == current_user.id
    ).first()

    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found"
        )

    update_data = reminder_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(reminder, field, value)

    db.commit()
    db.refresh(reminder)

    return reminder


# -----------------------------
# Enable Reminder
# -----------------------------

@router.patch("/{reminder_id}/enable")
def enable_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.user_id == current_user.id
    ).first()

    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found"
        )

    reminder.is_enabled = True

    db.commit()

    return {
        "message": "Reminder enabled successfully"
    }


# -----------------------------
# Disable Reminder
# -----------------------------

@router.patch("/{reminder_id}/disable")
def disable_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.user_id == current_user.id
    ).first()

    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found"
        )

    reminder.is_enabled = False

    db.commit()

    return {
        "message": "Reminder disabled successfully"
    }


# -----------------------------
# Delete Reminder
# -----------------------------

@router.delete("/{reminder_id}")
def delete_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.user_id == current_user.id
    ).first()

    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found"
        )

    db.delete(reminder)
    db.commit()

    return {
        "message": "Reminder deleted successfully"
    }


# -----------------------------
# Get Enabled Reminders
# -----------------------------

@router.get("/status/enabled")
def get_enabled_reminders(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    reminders = db.query(Reminder).filter(
        Reminder.user_id == current_user.id,
        Reminder.is_enabled.is_(True)
    ).all()

    return {
        "total_enabled": len(reminders),
        "reminders": reminders
    }
