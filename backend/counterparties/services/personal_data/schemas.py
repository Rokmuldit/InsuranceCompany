import uuid
from datetime import date
from pydantic import BaseModel, ConfigDict


class PersonalDataCreate(BaseModel):
    first_name: str
    last_name: str
    middle_name: str | None = None
    birth_date: date
    phone_number: str

    region: str
    city: str
    street: str
    house: str
    apartment: str | None = None


class PersonalDataUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    birth_date: date | None = None
    phone_number: str | None = None

    region: str | None = None
    city: str | None = None
    street: str | None = None
    house: str | None = None
    apartment: str | None = None


class PersonalDataResponse(BaseModel):
    id: uuid.UUID
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