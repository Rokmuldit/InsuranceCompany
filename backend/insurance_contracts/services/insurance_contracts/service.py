from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from insurance_contracts.services.insurance_contracts.repo import InsuranceContractsRepo
from insurance_contracts.services.insurance_contracts.schemas import (
    InsuranceContractCreate, InsuranceContractResponse
)
from utils.base_service import BaseService


class InsuranceContractsService(BaseService[InsuranceContractResponse]):
    response_schema = InsuranceContractResponse

    def __init__(self, session: AsyncSession):
        super().__init__(InsuranceContractsRepo(session))

    async def create_insurance_contract(self, contract_in: InsuranceContractCreate) -> InsuranceContractResponse:
        try:
            new_id = await self.repo.create_insurance_contract(
                plan_id=contract_in.plan_id,
                client_id=contract_in.client_id,
                agent_id=contract_in.agent_id
            )
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

        new_contract = await self._get_or_raise(
            self.repo.get_insurance_contract_by_id(new_id),
            detail="Помилка при створенні договору.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        return self.response_schema(**new_contract)

    async def get_insurance_contract_by_id(self, contract_id: uuid.UUID) -> InsuranceContractResponse:
        contract_data = await self._get_or_raise(
            self.repo.get_insurance_contract_by_id(contract_id),
            detail=f"Договір з ID {contract_id} не знайдено."
        )
        return self.response_schema(**contract_data)

    async def get_insurance_contracts_by_client_id(self, client_id: uuid.UUID) -> list[InsuranceContractResponse]:
        return self._map_list(await self.repo.get_insurance_contracts_by_client_id(client_id))

    async def get_insurance_contracts_by_agent_id(self, agent_id: uuid.UUID) -> list[InsuranceContractResponse]:
        return self._map_list(await self.repo.get_insurance_contracts_by_agent_id(agent_id))

    async def get_insurance_contracts_by_plan_id(self, plan_id: uuid.UUID) -> list[InsuranceContractResponse]:
        return self._map_list(await self.repo.get_insurance_contracts_by_plan_id(plan_id))

    async def get_all_insurance_contracts(self) -> list[InsuranceContractResponse]:
        return self._map_list(await self.repo.get_all_insurance_contracts())

    async def get_all_not_active_insurance_contracts(self) -> list[InsuranceContractResponse]:
        return self._map_list(await self.repo.get_all_not_active_insurance_contracts())

    async def activate_insurance_contract(self, contract_id: uuid.UUID) -> InsuranceContractResponse:
        existing_contract = await self._get_or_raise(
            self.repo.get_insurance_contract_by_id(contract_id),
            detail=f"Договір з ID {contract_id} не знайдено."
        )

        if existing_contract.get("is_active"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Договір вже активний."
            )

        await self.repo.activate_insurance_contract(contract_id)

        updated_contract = await self.repo.get_insurance_contract_by_id(contract_id)
        return self.response_schema(**updated_contract)

    async def delete_insurance_contract(self, contract_id: uuid.UUID) -> None:
        await self._get_or_raise(
            self.repo.get_insurance_contract_by_id(contract_id),
            detail=f"Договір з ID {contract_id} не знайдено."
        )
        await self.repo.delete_by_id(contract_id)

    async def get_quantity_of_active_insurance_contracts(self) -> int:
        return await self.repo.get_quantity_of_active_insurance_contracts()