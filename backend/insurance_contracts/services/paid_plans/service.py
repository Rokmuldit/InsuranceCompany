import uuid
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from insurance_contracts.services.paid_plans.repo import PaidPlansRepo
from insurance_contracts.services.paid_plans.schemas import (
    PaidPlanCreate, PaidPlanUpdate, PaidPlanResponse
)


class PaidPlansService:
    def __init__(self, session: AsyncSession):
        self.repo = PaidPlansRepo(session)

    async def create_paid_plan(self, plan_in: PaidPlanCreate) -> PaidPlanResponse:
        new_id = await self.repo.create_paid_plan(
            name=plan_in.name,
            payment_amount=plan_in.payment_amount,
            payment_period=plan_in.payment_period,
            description=plan_in.description
        )

        return PaidPlanResponse(id=new_id, **plan_in.model_dump())

    async def get_all_paid_plans(self) -> list[PaidPlanResponse]:
        plans_data = await self.repo.get_all_paid_plans()

        return [PaidPlanResponse(**plan) for plan in plans_data]

    async def get_paid_plan_by_id(self, plan_id: uuid.UUID) -> PaidPlanResponse:
        plan_data = await self.repo.get_paid_plan_by_id(plan_id)

        if not plan_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Тарифний план з ID {plan_id} не знайдено."
            )

        return PaidPlanResponse(**plan_data)

    async def update_paid_plan(
            self, plan_id: uuid.UUID, plan_in: PaidPlanUpdate
    ) -> PaidPlanResponse:
        existing_plan = await self.repo.get_paid_plan_by_id(plan_id)
        if not existing_plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Тарифний план з ID {plan_id} не знайдено. Оновлення неможливе."
            )

        await self.repo.update_paid_plan(
            plan_id=plan_id,
            name=plan_in.name,
            payment_amount=plan_in.payment_amount,
            payment_period=plan_in.payment_period,
            description=plan_in.description
        )

        return PaidPlanResponse(id=plan_id, **plan_in.model_dump())

    async def delete_paid_plan(self, plan_id: uuid.UUID) -> None:
        existing_plan = await self.repo.get_paid_plan_by_id(plan_id)
        if not existing_plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Тарифний план з ID {plan_id} не знайдено. Видалення неможливе."
            )

        await self.repo.delete_paid_plan(plan_id)