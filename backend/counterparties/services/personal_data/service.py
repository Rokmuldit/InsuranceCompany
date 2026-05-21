import uuid
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


from counterparties.services.personal_data.repo import PersonalDataRepo
from counterparties.services.personal_data.schemas import PersonalDataCreate, PersonalDataUpdate, PersonalDataResponse
from utils.base_service import BaseService


class PersonalDataService(BaseService[PersonalDataResponse]):
    response_schema = PersonalDataResponse

    def __init__(self, session: AsyncSession):
        super().__init__(PersonalDataRepo(session))

    async def create_personal_data(self, data_in: PersonalDataCreate) -> PersonalDataResponse:
        address_data = {
            "Region": data_in.region,
            "City": data_in.city,
            "Street": data_in.street,
            "House": data_in.house,
            "Apartment": data_in.apartment
        }
        pd_data = {
            "FirstName": data_in.first_name,
            "LastName": data_in.last_name,
            "MiddleName": data_in.middle_name,
            "BirthDate": data_in.birth_date,
            "PhoneNumber": data_in.phone_number
        }

        try:
            new_id = await self.repo.create_full(pd_data, address_data)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Помилка при створенні. Можливо, такий номер телефону вже існує."
            )

        new_record = await self._get_or_raise(
            self.repo.get_by_id(new_id),
            detail="Помилка при зчитуванні створеного запису.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        return self.response_schema(**new_record)

    async def get_all_personal_data(self) -> list[PersonalDataResponse]:
        data = await self.repo.get_all()
        return self._map_list(data)

    async def get_personal_data_by_id(self, pd_id: uuid.UUID) -> PersonalDataResponse:
        data = await self._get_or_raise(
            self.repo.get_by_id(pd_id),
            detail=f"Персональні дані з ID {pd_id} не знайдено."
        )
        return self.response_schema(**data)

    async def get_personal_data_by_client_id(self, client_id: uuid.UUID) -> PersonalDataResponse:
        data = await self._get_or_raise(
            self.repo.get_by_client_id(client_id),
            detail=f"Персональні дані для контрагента {client_id} не знайдено."
        )
        return self.response_schema(**data)

    async def update_personal_data(self, pd_id: uuid.UUID, data_in: PersonalDataUpdate) -> PersonalDataResponse:
        await self._get_or_raise(
            self.repo.get_by_id(pd_id),
            detail=f"Персональні дані з ID {pd_id} не знайдено."
        )

        update_dict = data_in.model_dump(exclude_unset=True)

        address_keys = {"region": "Region", "city": "City", "street": "Street", "house": "House",
                        "apartment": "Apartment"}
        pd_keys = {"first_name": "FirstName", "last_name": "LastName", "middle_name": "MiddleName",
                   "birth_date": "BirthDate", "phone_number": "PhoneNumber"}

        address_data = {address_keys[k]: v for k, v in update_dict.items() if k in address_keys}
        pd_data = {pd_keys[k]: v for k, v in update_dict.items() if k in pd_keys}

        try:
            await self.repo.update_full(pd_id, pd_data, address_data)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Помилка при оновленні. Перевірте унікальність номеру телефону."
            )

        updated_record = await self.repo.get_by_id(pd_id)
        return self.response_schema(**updated_record)

    async def delete_personal_data(self, pd_id: uuid.UUID) -> None:
        await self._get_or_raise(
            self.repo.get_by_id(pd_id),
            detail=f"Персональні дані з ID {pd_id} не знайдено."
        )
        await self.repo.delete_full(pd_id)