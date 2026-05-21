import uuid
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from insurance_contracts.services.insurance_payments.repo import InsurancePaymentsRepo
from insurance_contracts.services.insurance_payments.schemas import InsurancePaymentCreate, InsurancePaymentResponse
from utils.base_service import BaseService


class InsurancePaymentsService(BaseService[InsurancePaymentResponse]):
    response_schema = InsurancePaymentResponse

    def __init__(self, session: AsyncSession):
        super().__init__(InsurancePaymentsRepo(session))

    async def register_payment(self, payment_in: InsurancePaymentCreate) -> InsurancePaymentResponse:
        try:
            new_id = await self.repo.create_payment(
                contract_id=payment_in.contract_id,
                event_id=payment_in.event_id,
                payment_date=payment_in.payment_date,
                payment_amount=payment_in.payment_amount
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Не вдалося зареєструвати виплату. Перевірте правильність ID договору та події."
            )

        new_payment = await self._get_or_raise(
            self.repo.get_by_id(new_id),
            detail="Помилка при створенні страхової виплати.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        return self.response_schema(**new_payment)

    async def get_all_payments(self) -> list[InsurancePaymentResponse]:
        payments_data = await self.repo.get_all()
        return self._map_list(payments_data)

    async def delete_payment(self, payment_id: uuid.UUID) -> None:
        await self._get_or_raise(
            self.repo.get_by_id(payment_id),
            detail=f"Страхову виплату з ID {payment_id} не знайдено."
        )
        await self.repo.delete_by_id(payment_id)

    async def get_sum_all_payments(self) -> float:
        return await self.repo.get_sum_all_payments()