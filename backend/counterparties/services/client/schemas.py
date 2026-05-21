import uuid
from datetime import date
from pydantic import BaseModel, ConfigDict


class ClientCreate(BaseModel):
    personal_data_id: uuid.UUID


class ClientSearch(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    phone_number: str | None = None
    birth_date: date | None = None


class ClientResponse(BaseModel):
    id: uuid.UUID

    personal_data_id: uuid.UUID
    first_name: str
    last_name: str
    middle_name: str | None = None
    birth_date: date
    phone_number: str

    address_id: uuid.UUID
    region: str
    city: str
    street: str
    house: str
    apartment: str | None = None

    model_config = ConfigDict(from_attributes=True)