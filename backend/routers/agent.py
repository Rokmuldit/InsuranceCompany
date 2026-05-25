import uuid
from fastapi import APIRouter, status, Depends

from counterparties.services.agent.schemas import (
   AgentCreate, AgentSearch, AgentResponse
)
from counterparties.services.deps import AgentService
from utils.pagination import Page, PaginationParams

router = APIRouter(
    prefix="/agents",
    tags=["Agents"],
)

@router.post(
    "/",
    response_model=AgentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Створити агента"
)
async def create_agent(
    data_in: AgentCreate,
    service: AgentService
):
    return await service.create_agent(data_in)


@router.post(
    "/search",
    response_model=list[AgentResponse],
    summary="Складний пошук агентів"
)
async def search_agents(
    search_in: AgentSearch,
    service: AgentService
):
    return await service.search_agents(search_in)


@router.get(
    "/",
    response_model=Page[AgentResponse],
    summary="Отримати всіх агентів (пагіновано)"
)
async def get_all_agents(
    service: AgentService,
    pagination: PaginationParams = Depends()
):
    return await service.get_paginated_agents(
        page=pagination.page,
        size=pagination.size
    )


@router.get(
    "/{agent_id}",
    response_model=AgentResponse,
    summary="Отримати агента за ID"
)
async def get_agent_by_id(
    agent_id: uuid.UUID,
    service: AgentService
):
    return await service.get_agent_by_id(agent_id)


@router.delete(
    "/{agent_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Видалити агента"
)
async def delete_agent(
    agent_id: uuid.UUID,
    service: AgentService
):
    await service.delete_agent(agent_id)