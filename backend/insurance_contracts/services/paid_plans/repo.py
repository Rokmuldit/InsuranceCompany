import uuid
from decimal import Decimal
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class PaidPlansRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_paid_plan(
            self,
            name: str,
            payment_amount: Decimal | float,
            payment_period: str,
            description: str | None = None
    ) -> uuid.UUID | str:
        query = text("""
                     INSERT INTO PaidPlans (NAME, DESCRIPTION, PAYMENT_AMOUNT, PAYMENT_PERIOD)
                         OUTPUT INSERTED.ID
                     VALUES (:name, :description, :payment_amount, :payment_period)
                     """)

        result = await self.session.execute(query, {
            "name": name,
            "description": description,
            "payment_amount": payment_amount,
            "payment_period": payment_period
        })
        await self.session.commit()

        return result.scalar()

    async def get_all_paid_plans(self) -> list[dict]:
        query = text("""
                     SELECT ID             AS id,
                            NAME           AS name,
                            DESCRIPTION    AS description,
                            PAYMENT_AMOUNT AS payment_amount,
                            PAYMENT_PERIOD AS payment_period
                     FROM PaidPlans
                     """)
        result = await self.session.execute(query)

        return [dict(row) for row in result.mappings().all()]

    async def get_paid_plan_by_id(self, plan_id: uuid.UUID | str) -> dict | None:
        query = text("""
                     SELECT ID             AS id,
                            NAME           AS name,
                            DESCRIPTION    AS description,
                            PAYMENT_AMOUNT AS payment_amount,
                            PAYMENT_PERIOD AS payment_period
                     FROM PaidPlans
                     WHERE ID = :id
                     """)
        result = await self.session.execute(query, {"id": str(plan_id)})

        row = result.mappings().first()
        return dict(row) if row else None

    async def delete_paid_plan(self, plan_id: uuid.UUID | str) -> None:
        query = text("DELETE FROM PaidPlans WHERE ID = :id")
        await self.session.execute(query, {"id": str(plan_id)})
        await self.session.commit()

    async def update_paid_plan(
            self,
            plan_id: uuid.UUID | str,
            name: str,
            payment_amount: Decimal | float,
            payment_period: str,
            description: str | None = None
    ) -> None:
        query = text("""
                     UPDATE PaidPlans
                     SET NAME           = :name,
                         DESCRIPTION    = :description,
                         PAYMENT_AMOUNT = :payment_amount,
                         PAYMENT_PERIOD = :payment_period
                     WHERE ID = :id
                     """)
        await self.session.execute(query, {
            "id": str(plan_id),
            "name": name,
            "description": description,
            "payment_amount": payment_amount,
            "payment_period": payment_period
        })
        await self.session.commit()