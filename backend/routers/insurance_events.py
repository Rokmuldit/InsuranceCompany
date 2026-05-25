import uuid
from typing import Annotated
from fastapi import APIRouter, Depends, status

from insurance_contracts.services.insurance_events.schemas import (
    InsuranceEventCreate, InsuranceEventStatusUpdate, InsuranceEventResponse
)
from insurance_contracts.services.deps import InsuranceEventsService
from utils.pagination import Page, PaginationParams

router = APIRouter(
    prefix="/insurance-events",
    tags=["Insurance Events"],
)

@router.get(
    "/",
    response_model=Page[InsuranceEventResponse],
    summary="Отримати всі страхові події (пагіновано)"
)
async def get_all_events(
    service: InsuranceEventsService,
    pagination: PaginationParams = Depends()
):
    return await service.get_paginated_events(
        page=pagination.page,
        size=pagination.size
    )

@router.post(
    "/contract/{contract_id}",
    response_model=InsuranceEventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Зареєструвати страхову подію для договору"
)
async def register_event(
    contract_id: uuid.UUID,
    event_in: InsuranceEventCreate,
    service: InsuranceEventsService
):
    return await service.register_event(contract_id, event_in)


@router.get(
    "/contract/{contract_id}",
    response_model=Page[InsuranceEventResponse],
    summary="Отримати всі страхові події за ID договору (пагіновано)"
)
async def get_events_by_contract(
    contract_id: uuid.UUID,
    service: InsuranceEventsService,
    pagination: PaginationParams = Depends()
):
    return await service.get_paginated_events_by_contract(
        contract_id=contract_id,
        page=pagination.page,
        size=pagination.size
    )


@router.get(
    "/{event_id}",
    response_model=InsuranceEventResponse,
    summary="Отримати страхову подію за ID"
)
async def get_event(
    event_id: uuid.UUID,
    service: InsuranceEventsService
):
    return await service.get_event(event_id)


@router.patch(
    "/{event_id}/status",
    response_model=InsuranceEventResponse,
    summary="Визначити, чи є подія страховим випадком"
)
async def determine_insurance_case(
    event_id: uuid.UUID,
    status_in: InsuranceEventStatusUpdate,
    service: InsuranceEventsService
):
    return await service.determine_insurance_case(event_id, status_in)


@router.delete(
    "/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Видалити страхову подію"
)
async def delete_event(
    event_id: uuid.UUID,
    service: InsuranceEventsService
):
    await service.delete_event(event_id)

@router.get(
    "/sum/all_open_events"
)
async def get_sum_all_open_events(
    service: InsuranceEventsService
):
    return await service.get_sum_all_open_events()
