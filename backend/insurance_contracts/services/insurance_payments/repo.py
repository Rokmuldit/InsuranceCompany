import uuid
from datetime import date
from decimal import Decimal
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from utils.base_repo import BaseRepo


class InsurancePaymentsRepo(BaseRepo):
    table_name = "InsurancePayment"
    _BASE_QUERY = """
        SELECT 
            IP.ID AS id, 
            IP.PaymentDate AS payment_date, 
            IP.PaymentAmount AS payment_amount, 
            IP.ID_InsuranceContract AS contract_id, 
            IP.ID_InsuranceEvents AS event_id
        FROM InsurancePayment IP
    """

    async def create_payment(
            self, contract_id: uuid.UUID, event_id: uuid.UUID,
            payment_date: date, payment_amount: Decimal
    ) -> uuid.UUID | str:
        insert_query = """
            INSERT INTO InsurancePayment (PaymentDate, PaymentAmount, ID_InsuranceContract, ID_InsuranceEvents)
            OUTPUT INSERTED.ID
            VALUES (:payment_date, :payment_amount, :contract_id, :event_id)
        """
        result = await self.session.execute(text(insert_query), {
            "payment_date": payment_date,
            "payment_amount": payment_amount,
            "contract_id": str(contract_id),
            "event_id": str(event_id)
        })
        new_id = result.scalar()

        update_contract_query = "UPDATE InsuranceContract SET IsActive = 0 WHERE ID = :contract_id"
        await self.session.execute(text(update_contract_query), {"contract_id": str(contract_id)})

        await self.session.commit()
        return new_id

    async def get_all(self) -> list[dict]:
        return await self.find_all(self._BASE_QUERY)

    async def get_by_id(self, payment_id: uuid.UUID) -> dict | None:
        return await self.find_one(self._BASE_QUERY, {"IP.ID": str(payment_id)})

    async def get_sum_all_payments(self) -> float:
        query = f"SELECT SUM(PaymentAmount) FROM {self.table_name}"
        result = await self.session.execute(text(query))
        total = result.scalar()
        return float(total) if total is not None else 0.0