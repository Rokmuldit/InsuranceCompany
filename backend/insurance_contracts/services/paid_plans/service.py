import uuid
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from insurance_contracts.services.paid_plans.repo import PaidPlansRepo
from insurance_contracts.services.paid_plans.schemas import (
    PaidPlanCreate, PaidPlanUpdate, PaidPlanResponse
)
from utils.base_service import BaseService
from utils.pagination import Page


class PaidPlansService(BaseService[PaidPlanResponse]):
    response_schema = PaidPlanResponse

    def __init__(self, session: AsyncSession):
        super().__init__(PaidPlansRepo(session))

    async def get_paginated_paid_plans(self, page: int, size: int) -> Page[PaidPlanResponse]:
        return await self.get_paginated(
            page=page,
            size=size,
            base_query=self.repo._BASE_QUERY,
            order_by="ID"
        )

    async def create_paid_plan(self, plan_in: PaidPlanCreate) -> PaidPlanResponse:
        new_id = await self.repo.create_paid_plan(
            name=plan_in.name,
            payment_amount=plan_in.payment_amount,
            payment_period=plan_in.payment_period,
            description=plan_in.description
        )
        return self.response_schema(id=new_id, **plan_in.model_dump())

    async def get_all_paid_plans(self) -> list[PaidPlanResponse]:
        return self._map_list(await self.repo.get_all_paid_plans())

    async def get_paid_plan_by_id(self, plan_id: uuid.UUID) -> PaidPlanResponse:
        plan_data = await self._get_or_raise(
            self.repo.get_paid_plan_by_id(plan_id),
            detail=f"Тарифний план з ID {plan_id} не знайдено."
        )
        return self.response_schema(**plan_data)

    async def update_paid_plan(self, plan_id: uuid.UUID, plan_in: PaidPlanUpdate) -> PaidPlanResponse:
        await self._get_or_raise(
            self.repo.get_paid_plan_by_id(plan_id),
            detail=f"Тарифний план з ID {plan_id} не знайдено. Оновлення неможливе."
        )
        await self.repo.update_paid_plan(
            plan_id=plan_id,
            name=plan_in.name,
            payment_amount=plan_in.payment_amount,
            payment_period=plan_in.payment_period,
            description=plan_in.description
        )
        return self.response_schema(id=plan_id, **plan_in.model_dump())

    async def delete_paid_plan(self, plan_id: uuid.UUID) -> None:
        await self._get_or_raise(
            self.repo.get_paid_plan_by_id(plan_id),
            detail=f"Тарифний план з ID {plan_id} не знайдено. Видалення неможливе."
        )
        await self.repo.delete_by_id(plan_id)