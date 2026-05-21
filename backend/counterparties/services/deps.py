from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from counterparties.services.personal_data.service import PersonalDataService
from counterparties.services.client.service import ClientService
from counterparties.services.agent.service import AgentService

from database import get_async_session

async def get_personal_data_service(session: AsyncSession = Depends(get_async_session)) -> PersonalDataService:
    return PersonalDataService(session)

async def get_client_service(session: AsyncSession = Depends(get_async_session)) -> ClientService:
    return ClientService(session)

async def get_agent_service(session: AsyncSession = Depends(get_async_session)) -> AgentService:
    return AgentService(session)

PersonalDataService = Annotated[PersonalDataService, Depends(get_personal_data_service)]
ClientService = Annotated[ClientService, Depends(get_client_service)]
AgentService = Annotated[AgentService, Depends(get_agent_service)]