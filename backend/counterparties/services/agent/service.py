import uuid
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from counterparties.services.agent.repo import AgentRepo
from counterparties.services.agent.schemas import AgentCreate, AgentSearch, AgentResponse
from utils.base_service import BaseService


class AgentService(BaseService[AgentResponse]):
    response_schema = AgentResponse

    def __init__(self, session: AsyncSession):
        super().__init__(AgentRepo(session))

    async def create_agent(self, data_in: AgentCreate) -> AgentResponse:
        try:
            new_id = await self.repo.create_agent(data_in.client_id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Не вдалося створити агента. Перевірте, чи існує вказаний ID клієнта."
            )

        new_agent = await self._get_or_raise(
            self.repo.get_by_id(new_id),
            detail="Помилка при зчитуванні даних нового агента.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        return self.response_schema(**new_agent)

    async def get_all_agents(self) -> list[AgentResponse]:
        agents_data = await self.repo.get_all()
        return self._map_list(agents_data)

    async def get_agent_by_id(self, agent_id: uuid.UUID) -> AgentResponse:
        agent_data = await self._get_or_raise(
            self.repo.get_by_id(agent_id),
            detail=f"Агента з ID {agent_id} не знайдено."
        )
        return self.response_schema(**agent_data)

    async def search_agents(self, search_in: AgentSearch) -> list[AgentResponse]:
        search_dict = search_in.model_dump(exclude_unset=True, exclude_none=True)

        search_mapping = {
            "first_name": "PD.FirstName",
            "last_name": "PD.LastName",
            "middle_name": "PD.MiddleName",
            "phone_number": "PD.PhoneNumber",
            "birth_date": "PD.BirthDate"
        }

        db_filters = {
            search_mapping[k]: v
            for k, v in search_dict.items()
            if k in search_mapping
        }

        results = await self.repo.search_complex(db_filters)
        return self._map_list(results)

    async def delete_agent(self, agent_id: uuid.UUID) -> None:
        await self._get_or_raise(
            self.repo.get_by_id(agent_id),
            detail=f"Агента з ID {agent_id} не знайдено."
        )

        try:
            await self.repo.delete_by_id(agent_id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Неможливо видалити агента. Можливо, він закріплений за діючими договорами страхування."
            )