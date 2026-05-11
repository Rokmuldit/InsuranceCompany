import uuid
from decimal import Decimal
from utils.base_repo import BaseRepo


class PaidPlansRepo(BaseRepo):
    table_name = "PaidPlans"
    _BASE_QUERY = """
        SELECT ID AS id, NAME AS name, DESCRIPTION AS description, 
               PAYMENT_AMOUNT AS payment_amount, PAYMENT_PERIOD AS payment_period
        FROM PaidPlans
    """

    async def create_paid_plan(
            self, name: str, payment_amount: Decimal | float,
            payment_period: str, description: str | None = None
    ) -> uuid.UUID | str:
        return await self.create_record(
            NAME=name, DESCRIPTION=description,
            PAYMENT_AMOUNT=payment_amount, PAYMENT_PERIOD=payment_period
        )

    async def update_paid_plan(
            self, plan_id: uuid.UUID | str, name: str,
            payment_amount: Decimal | float, payment_period: str,
            description: str | None = None
    ) -> None:
        await self.update_record(
            record_id=plan_id, NAME=name, DESCRIPTION=description,
            PAYMENT_AMOUNT=payment_amount, PAYMENT_PERIOD=payment_period
        )

    async def get_all_paid_plans(self) -> list[dict]:
        return await self.find_all(self._BASE_QUERY)

    async def get_paid_plan_by_id(self, plan_id: uuid.UUID | str) -> dict | None:
        return await self.find_one(self._BASE_QUERY, {"ID": str(plan_id)})