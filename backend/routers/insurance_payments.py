import uuid
from fastapi import APIRouter, status, Depends

from insurance_contracts.services.insurance_payments.schemas import (
    InsurancePaymentCreate, InsurancePaymentResponse
)
from insurance_contracts.services.deps import InsurancePaymentsService
from utils.pagination import Page, PaginationParams

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
    response_model=Page[InsurancePaymentResponse],
    summary="Отримати всі страхові виплати (пагіновано)"
)
async def get_all_payments(
    service: InsurancePaymentsService,
    pagination: PaginationParams = Depends()
):
    return await service.get_paginated_payments(
        page=pagination.page,
        size=pagination.size
    )


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