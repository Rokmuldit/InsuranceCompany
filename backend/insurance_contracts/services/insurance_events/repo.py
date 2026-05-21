import uuid
from datetime import date
from utils.base_repo import BaseRepo


class InsuranceEventsRepo(BaseRepo):
    table_name = "InsuranceEvents"
    _BASE_QUERY = """
        SELECT 
            IE.ID AS id, 
            IE.EventDate AS event_date, 
            IE.IsInsuranceCase AS is_insurance_case, 
            IE.Description AS description, 
            IE.ID_InsuranceContract AS contract_id
        FROM InsuranceEvents IE
    """

    async def create_insurance_event(
            self, contract_id: uuid.UUID, event_date: date, description: str | None = None
    ) -> uuid.UUID | str:
        return await self.create_record(
            EventDate=event_date,
            Description=description,
            IsInsuranceCase=0,
            ID_InsuranceContract=str(contract_id)
        )

    async def update_is_insurance_case(self, event_id: uuid.UUID, is_insurance_case: bool) -> None:
        await self.update_record(
            record_id=event_id,
            IsInsuranceCase=1 if is_insurance_case else 0
        )

    async def get_by_id(self, event_id: uuid.UUID) -> dict | None:
        return await self.find_one(self._BASE_QUERY, {"IE.ID": str(event_id)})

    async def get_by_contract_id(self, contract_id: uuid.UUID) -> list[dict]:
        return await self.find_all(self._BASE_QUERY, {"IE.ID_InsuranceContract": str(contract_id)})

    async def get_sum_all_open_events(self) -> int:
        query = f"SELECT COUNT(*) FROM {self.table_name} WHERE IsInsuranceCase = 0"
        result = await self.session.execute(query)
        return result.scalar()