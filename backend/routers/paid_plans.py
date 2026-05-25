import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from insurance_contracts.services.paid_plans.schemas import (
    PaidPlanCreate, PaidPlanUpdate, PaidPlanResponse
)
from insurance_contracts.services.deps import PaidPlansService
from utils.pagination import Page, PaginationParams

router = APIRouter(
    prefix="/paid-plans",
    tags=["Paid Plans"],
)

@router.post(
    "/",
    response_model=PaidPlanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Створити тарифний план"
)
async def create_paid_plan(
    plan_in: PaidPlanCreate,
    service: PaidPlansService
):
    return await service.create_paid_plan(plan_in)


@router.get(
    "/",
    response_model=Page[PaidPlanResponse],
    summary="Отримати всі тарифні плани (пагіновано)"
)
async def get_all_paid_plans(
    service: PaidPlansService,
    pagination: PaginationParams = Depends()
):
    return await service.get_paginated_paid_plans(
        page=pagination.page,
        size=pagination.size
    )


@router.get(
    "/{plan_id}",
    response_model=PaidPlanResponse,
    summary="Отримати тарифний план за ID"
)
async def get_paid_plan_by_id(
    plan_id: uuid.UUID,
    service: PaidPlansService
):
    return await service.get_paid_plan_by_id(plan_id)


@router.put(
    "/{plan_id}",
    response_model=PaidPlanResponse,
    summary="Оновити існуючий тарифний план"
)
async def update_paid_plan(
    plan_id: uuid.UUID,
    plan_in: PaidPlanUpdate,
    service: PaidPlansService
):
    return await service.update_paid_plan(plan_id, plan_in)


@router.delete(
    "/{plan_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Видалити тарифний план"
)
async def delete_paid_plan(
    plan_id: uuid.UUID,
    service: PaidPlansService
):
    await service.delete_paid_plan(plan_id)