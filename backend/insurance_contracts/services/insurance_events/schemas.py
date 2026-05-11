import uuid
from datetime import date
from pydantic import BaseModel, ConfigDict


class InsuranceEventCreate(BaseModel):
    event_date: date
    description: str | None = None


class InsuranceEventStatusUpdate(BaseModel):
    is_insurance_case: bool


class InsuranceEventResponse(BaseModel):
    id: uuid.UUID
    event_date: date
    is_insurance_case: bool
    description: str | None = None
    contract_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)