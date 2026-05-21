from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from insurance_contracts.services.insurance_payments.service import InsurancePaymentsService
from insurance_contracts.services.paid_plans.service import PaidPlansService
from insurance_contracts.services.insurance_contracts.service import InsuranceContractsService
from insurance_contracts.services.insurance_events.service import InsuranceEventsService
from database import get_async_session

async def get_paid_plans_service(session: AsyncSession = Depends(get_async_session)) -> PaidPlansService:
    return PaidPlansService(session)

async def get_insurance_contracts_service(session: AsyncSession = Depends(get_async_session)) -> InsuranceContractsService:
    return InsuranceContractsService(session)

async def get_insurance_events_service(session: AsyncSession = Depends(get_async_session)) -> InsuranceEventsService:
    return InsuranceEventsService(session)

async def get_insurance_payments_service(session: AsyncSession = Depends(get_async_session)) -> InsurancePaymentsService:
    return InsurancePaymentsService(session)

PaidPlansService = Annotated[PaidPlansService, Depends(get_paid_plans_service)]
InsuranceContractsService = Annotated[InsuranceContractsService, Depends(get_insurance_contracts_service)]
InsuranceEventsService = Annotated[InsuranceEventsService, Depends(get_insurance_events_service)]
InsurancePaymentsService = Annotated[InsurancePaymentsService, Depends(get_insurance_payments_service)]