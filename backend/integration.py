

from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from Database import get_db
from Models import Integration
from Schemas import IntegrationCreate, IntegrationResponse, ActivitySync
from Security import get_current_user
from Config import settings

router = APIRouter(tags=["Fitness Integrations"])


SUPPORTED_PROVIDERS = ["google_fit", "apple_health"]


# -----------------------------
# Connect Integration
# -----------------------------

@router.post(
    "/connect",
    response_model=IntegrationResponse,
    status_code=status.HTTP_201_CREATED
)
def connect_integration(
    integration_data: IntegrationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    provider = integration_data.provider.lower()

    if provider not in SUPPORTED_PROVIDERS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported integration provider"
        )

    if provider == "google_fit" and not settings.GOOGLE_FIT_ENABLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google Fit integration is currently disabled"
        )

    if provider == "apple_health" and not settings.APPLE_HEALTH_ENABLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Apple Health integration is currently disabled"
        )

    existing = db.query(Integration).filter(
        Integration.user_id == current_user.id,
        Integration.provider == provider
    ).first()

    if existing:
        existing.is_connected = True
        existing.connected_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(existing)
        return existing

    new_integration = Integration(
        user_id=current_user.id,
        provider=provider,
        is_connected=True,
        connected_at=datetime.now(timezone.utc)
    )

    db.add(new_integration)
    db.commit()
    db.refresh(new_integration)

    return new_integration


# -----------------------------
# Get Connected Integrations
# -----------------------------

@router.get("/", response_model=list[IntegrationResponse])
def get_integrations(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Integration).filter(
        Integration.user_id == current_user.id
    ).all()


# -----------------------------
# Sync Fitness Activity
# -----------------------------

@router.post("/sync")
def sync_activity(
    activity_data: ActivitySync,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    integration = db.query(Integration).filter(
        Integration.user_id == current_user.id,
        Integration.provider == activity_data.provider.lower(),
        Integration.is_connected.is_(True)
    ).first()

    if not integration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connected integration not found"
        )

    # This endpoint accepts activity data from a trusted integration
    # client. Real provider API synchronization must be implemented
    # separately using the provider's authentication and API.
    integration.last_synced_at = datetime.now(timezone.utc)

    db.commit()

    return {
        "message": "Activity data received successfully",
        "provider": integration.provider,
        "steps": activity_data.steps,
        "active_minutes": activity_data.active_minutes,
        "calories_burned": activity_data.calories_burned,
        "synced_at": integration.last_synced_at,
        "note": "Provider API synchronization must be configured separately."
    }


# -----------------------------
# Get Integration Status
# -----------------------------

@router.get("/status")
def get_integration_status(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    integrations = db.query(Integration).filter(
        Integration.user_id == current_user.id
    ).all()

    return {
        "integrations": [
            {
                "provider": item.provider,
                "is_connected": item.is_connected,
                "connected_at": item.connected_at,
                "last_synced_at": item.last_synced_at
            }
            for item in integrations
        ]
    }


# -----------------------------
# Disconnect Integration
# -----------------------------

@router.delete("/{provider}")
def disconnect_integration(
    provider: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    integration = db.query(Integration).filter(
        Integration.user_id == current_user.id,
        Integration.provider == provider.lower()
    ).first()

    if not integration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Integration not found"
        )

    integration.is_connected = False

    db.commit()

    return {
        "message": f"{provider} disconnected successfully"
    }
