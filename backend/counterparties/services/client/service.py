import uuid
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from counterparties.services.client.repo import ClientRepo
from counterparties.services.client.schemas import ClientCreate, ClientSearch, ClientResponse
from utils.base_service import BaseService


class ClientService(BaseService[ClientResponse]):
    response_schema = ClientResponse

    def __init__(self, session: AsyncSession):
        super().__init__(ClientRepo(session))

    async def create_client(self, data_in: ClientCreate) -> ClientResponse:
        try:
            new_id = await self.repo.create_client(data_in.personal_data_id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Не вдалося створити клієнта. Перевірте, чи існує вказаний ID персональних даних."
            )

        new_client = await self._get_or_raise(
            self.repo.get_by_id(new_id),
            detail="Помилка при створенні клієнта.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        return self.response_schema(**new_client)

    async def get_all_clients(self) -> list[ClientResponse]:
        clients_data = await self.repo.get_all()
        return self._map_list(clients_data)

    async def get_client_by_id(self, client_id: uuid.UUID) -> ClientResponse:
        client_data = await self._get_or_raise(
            self.repo.get_by_id(client_id),
            detail=f"Клієнта з ID {client_id} не знайдено."
        )
        return self.response_schema(**client_data)

    async def search_clients(self, search_in: ClientSearch) -> list[ClientResponse]:
        search_dict = search_in.model_dump(exclude_unset=True, exclude_none=True)

        search_mapping = {
            "first_name": "PD.FirstName",
            "last_name": "PD.LastName",
            "middle_name": "PD.MiddleName",
            "phone_number": "PD.PhoneNumber",
            "birth_date": "PD.BirthDate"
        }

        db_filters = {
            search_mapping[k]: v
            for k, v in search_dict.items()
            if k in search_mapping
        }

        results = await self.repo.search_complex(db_filters)
        return self._map_list(results)

    async def delete_client(self, client_id: uuid.UUID) -> None:
        await self._get_or_raise(
            self.repo.get_by_id(client_id),
            detail=f"Клієнта з ID {client_id} не знайдено."
        )

        try:
            await self.repo.delete_by_id(client_id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Неможливо видалити клієнта. Можливо, до нього прив'язані договори або агенти."
            )
    async def get_sum_of_all_clients(self) -> float:
        return await self.repo.get_sum_of_all_clients()