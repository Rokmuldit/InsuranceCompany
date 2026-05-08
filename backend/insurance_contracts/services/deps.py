from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from insurance_contracts.services.paid_plans.service import PaidPlansService
from database import get_async_session

async def get_paid_plans_service(session: AsyncSession = Depends(get_async_session)) -> PaidPlansService:
    return PaidPlansService(session)

PaidPlansService = Annotated[PaidPlansService, Depends(get_paid_plans_service)]