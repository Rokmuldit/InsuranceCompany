import uuid
from fastapi import APIRouter, status, Depends

from counterparties.services.client.schemas import (
    ClientCreate, ClientSearch, ClientResponse
)
from counterparties.services.deps import ClientService
from utils.pagination import Page, PaginationParams

router = APIRouter(
    prefix="/clients",
    tags=["Clients"],
)

@router.post(
    "/",
    response_model=ClientResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Створити клієнта"
)
async def create_client(
    data_in: ClientCreate,
    service: ClientService
):
    return await service.create_client(data_in)


@router.post(
    "/search",
    response_model=list[ClientResponse],
    summary="Складний пошук клієнтів"
)
async def search_clients(
    search_in: ClientSearch,
    service: ClientService
):
    return await service.search_clients(search_in)


@router.get(
    "/",
    response_model=Page[ClientResponse],
    summary="Отримати всіх клієнтів (пагіновано)"
)
async def get_all_clients(
    service: ClientService,
    pagination: PaginationParams = Depends()
):
    return await service.get_paginated_clients(
        page=pagination.page,
        size=pagination.size
    )


@router.get(
    "/{client_id}",
    response_model=ClientResponse,
    summary="Отримати клієнта за ID"
)
async def get_client_by_id(
    client_id: uuid.UUID,
    service: ClientService
):
    return await service.get_client_by_id(client_id)


@router.delete(
    "/{client_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Видалити клієнта"
)
async def delete_client(
    client_id: uuid.UUID,
    service: ClientService
):
    await service.delete_client(client_id)

@router.get(
    "/sum/all"
)
async def get_sum_all_clients(
    service: ClientService
):
    return await service.get_sum_of_all_clients()