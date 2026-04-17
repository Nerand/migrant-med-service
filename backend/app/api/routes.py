from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.config import ALLOWED_POLICY_COUNTRIES, PURPOSES
from app.db.database import get_db
from app.models.recommendation import RecommendationRequest
from app.schemas.recommendation import (
    RecommendationHistoryItem,
    RecommendationRequestIn,
    RecommendationResponse,
)
from app.services.rules import RequirementEngine

router = APIRouter(prefix="/api/v1")


@router.get("/health")
def healthcheck():
    return {"status": "ok"}


@router.get("/reference/countries")
def get_countries():
    return {
        "policy_countries": sorted(list(ALLOWED_POLICY_COUNTRIES)),
    }


@router.get("/reference/purposes")
def get_purposes():
    return {
        "purposes": PURPOSES,
    }


@router.post("/recommendations", response_model=RecommendationResponse)
def create_recommendation(payload: RecommendationRequestIn, db: Session = Depends(get_db)):
    result = RequirementEngine.evaluate(payload)

    medical = next(item for item in result.requirements if item.code == "medical_examination")
    insurance = next(item for item in result.requirements if item.code == "insurance_policy")

    record = RecommendationRequest(
        citizenship=payload.citizenship,
        purpose_of_entry=payload.purpose_of_entry,
        entry_date=payload.entry_date,
        stay_duration_days=payload.stay_duration_days,
        has_insurance=payload.has_insurance,
        employment_related=payload.employment_related,
        medical_required=medical.required,
        medical_deadline=medical.deadline,
        medical_place=medical.place,
        medical_reason=medical.reason,
        insurance_required=insurance.required,
        insurance_deadline=insurance.deadline,
        insurance_place=insurance.place,
        insurance_reason=insurance.reason,
    )
    db.add(record)
    db.commit()

    return result


@router.get("/history", response_model=list[RecommendationHistoryItem])
def get_history(db: Session = Depends(get_db)):
    rows = db.query(RecommendationRequest).order_by(RecommendationRequest.id.desc()).all()
    return [
        RecommendationHistoryItem(
            id=row.id,
            citizenship=row.citizenship,
            purpose_of_entry=row.purpose_of_entry,
            entry_date=row.entry_date,
            stay_duration_days=row.stay_duration_days,
            has_insurance=row.has_insurance,
            employment_related=row.employment_related,
            medical_required=row.medical_required,
            insurance_required=row.insurance_required,
            created_at=row.created_at.isoformat() if row.created_at else "",
        )
        for row in rows
    ]
