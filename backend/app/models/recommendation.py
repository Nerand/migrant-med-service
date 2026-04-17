from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from app.db.database import Base


class RecommendationRequest(Base):
    __tablename__ = "recommendation_requests"

    id = Column(Integer, primary_key=True, index=True)
    citizenship = Column(String(100), nullable=False)
    purpose_of_entry = Column(String(100), nullable=False)
    entry_date = Column(String(30), nullable=False)
    stay_duration_days = Column(Integer, nullable=False)
    has_insurance = Column(Boolean, nullable=False)
    employment_related = Column(Boolean, nullable=False)

    medical_required = Column(Boolean, nullable=False)
    medical_deadline = Column(Text, nullable=True)
    medical_place = Column(Text, nullable=True)
    medical_reason = Column(Text, nullable=True)

    insurance_required = Column(Boolean, nullable=False)
    insurance_deadline = Column(Text, nullable=True)
    insurance_place = Column(Text, nullable=True)
    insurance_reason = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
