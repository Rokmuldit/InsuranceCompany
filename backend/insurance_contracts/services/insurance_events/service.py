import uuid
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from insurance_contracts.services.insurance_events.repo import InsuranceEventsRepo
from insurance_contracts.services.insurance_events.schemas import InsuranceEventCreate, InsuranceEventStatusUpdate, InsuranceEventResponse
from utils.base_service import BaseService
from utils.pagination import Page


class InsuranceEventsService(BaseService[InsuranceEventResponse]):
    response_schema = InsuranceEventResponse

    def __init__(self, session: AsyncSession):
        super().__init__(InsuranceEventsRepo(session))

    async def get_paginated_events(self, page: int, size: int) -> Page[InsuranceEventResponse]:
        return await self.get_paginated(
            page=page,
            size=size,
            base_query=self.repo._BASE_QUERY,
            order_by="IE.ID"
        )

    async def get_paginated_events_by_contract(
            self, contract_id: uuid.UUID, page: int, size: int
    ) -> Page[InsuranceEventResponse]:
        return await self.get_paginated(
            page=page,
            size=size,
            base_query=self.repo._BASE_QUERY,
            filters={"IE.ID_InsuranceContract": str(contract_id)},
            order_by="IE.ID"
        )

    async def register_event(
            self, contract_id: uuid.UUID, event_in: InsuranceEventCreate
    ) -> InsuranceEventResponse:
        try:
            new_id = await self.repo.create_insurance_event(
                contract_id=contract_id,
                event_date=event_in.event_date,
                description=event_in.description
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Не вдалося створити подію. Перевірте правильність ID договору."
            )

        new_event = await self._get_or_raise(
            self.repo.get_by_id(new_id),
            detail="Помилка при створенні події.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        return self.response_schema(**new_event)

    async def determine_insurance_case(
            self, event_id: uuid.UUID, status_in: InsuranceEventStatusUpdate
    ) -> InsuranceEventResponse:
        await self._get_or_raise(
            self.repo.get_by_id(event_id),
            detail=f"Страхову подію з ID {event_id} не знайдено."
        )

        await self.repo.update_is_insurance_case(event_id, status_in.is_insurance_case)

        updated_event = await self.repo.get_by_id(event_id)
        return self.response_schema(**updated_event)

    async def get_event(self, event_id: uuid.UUID) -> InsuranceEventResponse:
        event_data = await self._get_or_raise(
            self.repo.get_by_id(event_id),
            detail=f"Страхову подію з ID {event_id} не знайдено."
        )
        return self.response_schema(**event_data)

    async def get_events_by_contract(self, contract_id: uuid.UUID) -> list[InsuranceEventResponse]:
        events_data = await self.repo.get_by_contract_id(contract_id)
        return self._map_list(events_data)

    async def delete_event(self, event_id: uuid.UUID) -> None:
        await self._get_or_raise(
            self.repo.get_by_id(event_id),
            detail=f"Страхову подію з ID {event_id} не знайдено."
        )
        await self.repo.delete_by_id(event_id)

    async def get_sum_all_open_events(self) -> int:
        return await self.repo.get_sum_all_open_events()