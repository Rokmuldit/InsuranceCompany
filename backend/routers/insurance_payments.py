import uuid
from fastapi import APIRouter, status

from insurance_contracts.services.insurance_payments.schemas import (
    InsurancePaymentCreate, InsurancePaymentResponse
)
from insurance_contracts.services.deps import InsurancePaymentsService

router = APIRouter(
    prefix="/insurance-payments",
    tags=["Insurance Payments"],
)

@router.post(
    "/",
    response_model=InsurancePaymentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Зареєструвати страхову виплату"
)
async def register_payment(
    payment_in: InsurancePaymentCreate,
    service: InsurancePaymentsService
):
    return await service.register_payment(payment_in)


@router.get(
    "/",
    response_model=list[InsurancePaymentResponse],
    summary="Отримати всі страхові виплати"
)
async def get_all_payments(
    service: InsurancePaymentsService
):
    return await service.get_all_payments()


@router.delete(
    "/{payment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Видалити страхову виплату"
)
async def delete_payment(
    payment_id: uuid.UUID,
    service: InsurancePaymentsService
):
    await service.delete_payment(payment_id)

@router.get(
    "/sum/all"
)
async def get_sum_all_payments(
    service: InsurancePaymentsService
):
    return await service.get_sum_all_payments()