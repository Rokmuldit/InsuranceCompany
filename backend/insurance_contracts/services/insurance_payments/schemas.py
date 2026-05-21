import uuid
from datetime import date
from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class InsurancePaymentCreate(BaseModel):
    contract_id: uuid.UUID
    event_id: uuid.UUID
    payment_date: date
    payment_amount: Decimal


class InsurancePaymentResponse(BaseModel):
    id: uuid.UUID
    payment_date: date
    payment_amount: Decimal
    contract_id: uuid.UUID
    event_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)