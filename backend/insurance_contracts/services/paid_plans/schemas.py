import uuid
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict


class PaidPlanBase(BaseModel):
    name: str = Field(..., max_length=50, description="Назва тарифного плану")
    description: str | None = Field(None, description="Опис тарифного плану")
    payment_amount: Decimal = Field(
        ..., max_digits=10, decimal_places=2, description="Сума оплати"
    )
    payment_period: str = Field(..., max_length=50, description="Період оплати")


class PaidPlanCreate(PaidPlanBase):
    pass


class PaidPlanUpdate(PaidPlanBase):
    pass


class PaidPlanResponse(PaidPlanBase):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)