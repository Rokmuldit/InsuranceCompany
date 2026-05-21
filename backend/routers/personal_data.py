import uuid
from fastapi import APIRouter, status

from counterparties.services.personal_data.schemas import (
    PersonalDataCreate, PersonalDataUpdate, PersonalDataResponse
)
from counterparties.services.deps import PersonalDataService

router = APIRouter(
    prefix="/personal-data",
    tags=["Personal Data"],
)

@router.post(
    "/",
    response_model=PersonalDataResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Створити персональні дані та адресу"
)
async def create_personal_data(
    data_in: PersonalDataCreate,
    service: PersonalDataService
):
    return await service.create_personal_data(data_in)


@router.get(
    "/",
    response_model=list[PersonalDataResponse],
    summary="Отримати всі персональні дані"
)
async def get_all_personal_data(
    service: PersonalDataService
):
    return await service.get_all_personal_data()


@router.get(
    "/client/{client_id}",
    response_model=PersonalDataResponse,
    summary="Отримати персональні дані за ID контрагента (клієнта)"
)
async def get_personal_data_by_client_id(
    client_id: uuid.UUID,
    service: PersonalDataService
):
    return await service.get_personal_data_by_client_id(client_id)


@router.get(
    "/{pd_id}",
    response_model=PersonalDataResponse,
    summary="Отримати персональні дані за ID"
)
async def get_personal_data_by_id(
    pd_id: uuid.UUID,
    service: PersonalDataService
):
    return await service.get_personal_data_by_id(pd_id)


@router.patch(
    "/{pd_id}",
    response_model=PersonalDataResponse,
    summary="Частково оновити персональні дані та/або адресу"
)
async def update_personal_data(
    pd_id: uuid.UUID,
    data_in: PersonalDataUpdate,
    service: PersonalDataService
):
    return await service.update_personal_data(pd_id, data_in)


@router.delete(
    "/{pd_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Видалити персональні дані та пов'язану адресу"
)
async def delete_personal_data(
    pd_id: uuid.UUID,
    service: PersonalDataService
):
    await service.delete_personal_data(pd_id)