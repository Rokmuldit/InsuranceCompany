import uuid
from datetime import date
from decimal import Decimal
from pydantic import BaseModel, ConfigDict

class InsuranceContractCreate(BaseModel):
    plan_id: uuid.UUID
    client_id: uuid.UUID
    agent_id: uuid.UUID


class InsuranceContractResponse(BaseModel):
    contract_id: uuid.UUID
    contract_amount: Decimal
    start_date: date
    end_date: date
    is_active: bool

    client_id: uuid.UUID
    client_first_name: str
    client_last_name: str
    client_middle_name: str | None = None
    client_birth_date: date
    client_phone_number: str
    client_region: str
    client_city: str
    client_street: str
    client_house: str
    client_apartment: str | None = None

    agent_id: uuid.UUID
    agent_first_name: str
    agent_last_name: str
    agent_middle_name: str | None = None
    agent_birth_date: date
    agent_phone_number: str
    agent_region: str
    agent_city: str
    agent_street: str
    agent_house: str
    agent_apartment: str | None = None

    model_config = ConfigDict(from_attributes=True)