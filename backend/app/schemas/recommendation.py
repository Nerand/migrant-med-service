from pydantic import BaseModel, Field


class RecommendationRequestIn(BaseModel):
    citizenship: str = Field(min_length=1, max_length=100)
    purpose_of_entry: str = Field(min_length=1, max_length=100)
    entry_date: str = Field(min_length=1, max_length=30)
    stay_duration_days: int = Field(ge=1, le=3650)
    has_insurance: bool
    employment_related: bool


class RequirementItem(BaseModel):
    code: str
    title: str
    required: bool
    deadline: str | None = None
    place: str | None = None
    reason: str


class RecommendationSummary(BaseModel):
    required_count: int
    optional_count: int


class RecommendationResponse(BaseModel):
    profile: RecommendationRequestIn
    requirements: list[RequirementItem]
    summary: RecommendationSummary


class RecommendationHistoryItem(BaseModel):
    id: int
    citizenship: str
    purpose_of_entry: str
    entry_date: str
    stay_duration_days: int
    has_insurance: bool
    employment_related: bool
    medical_required: bool
    insurance_required: bool
    created_at: str

    class Config:
        from_attributes = True
