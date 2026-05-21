import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from insurance_contracts.services.deps import InsuranceContractsService
from insurance_contracts.services.insurance_contracts.schemas import (
    InsuranceContractCreate, InsuranceContractResponse
)

router = APIRouter(
    prefix="/insurance-contracts",
    tags=["Insurance Contracts"],
)


@router.post(
    "/",
    response_model=InsuranceContractResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Створити новий договір страхування"
)
async def create_insurance_contract(
    contract_in: InsuranceContractCreate,
    service: InsuranceContractsService
):
    return await service.create_insurance_contract(contract_in)


@router.get(
    "/",
    response_model=list[InsuranceContractResponse],
    summary="Отримати всі договори страхування"
)
async def get_all_insurance_contracts(
    service: InsuranceContractsService
):
    return await service.get_all_insurance_contracts()


@router.get(
    "/not-active",
    response_model=list[InsuranceContractResponse],
    summary="Отримати всі неактивні договори страхування"
)
async def get_all_not_active_insurance_contracts(
    service: InsuranceContractsService
):
    return await service.get_all_not_active_insurance_contracts()


@router.get(
    "/{contract_id}",
    response_model=InsuranceContractResponse,
    summary="Отримати договір страхування за ID"
)
async def get_insurance_contract_by_id(
    contract_id: uuid.UUID,
    service: InsuranceContractsService
):
    return await service.get_insurance_contract_by_id(contract_id)


@router.get(
    "/client/{client_id}",
    response_model=list[InsuranceContractResponse],
    summary="Отримати договори страхування за ID клієнта"
)
async def get_insurance_contracts_by_client_id(
    client_id: uuid.UUID,
    service: InsuranceContractsService
):
    return await service.get_insurance_contracts_by_client_id(client_id)


@router.get(
    "/agent/{agent_id}",
    response_model=list[InsuranceContractResponse],
    summary="Отримати договори страхування за ID агента"
)
async def get_insurance_contracts_by_agent_id(
    agent_id: uuid.UUID,
    service: InsuranceContractsService
):
    return await service.get_insurance_contracts_by_agent_id(agent_id)


@router.get(
    "/plan/{plan_id}",
    response_model=list[InsuranceContractResponse],
    summary="Отримати договори страхування за ID тарифного плану"
)
async def get_insurance_contracts_by_plan_id(
    plan_id: uuid.UUID,
    service: InsuranceContractsService
):
    return await service.get_insurance_contracts_by_plan_id(plan_id)


@router.patch(
    "/{contract_id}/activate",
    response_model=InsuranceContractResponse,
    summary="Активувати договір страхування"
)
async def activate_insurance_contract(
    contract_id: uuid.UUID,
    service: InsuranceContractsService
):
    return await service.activate_insurance_contract(contract_id)


@router.delete(
    "/{contract_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Видалити договір страхування"
)
async def delete_insurance_contract(
    contract_id: uuid.UUID,
    service: InsuranceContractsService
):
    await service.delete_insurance_contract(contract_id)

@router.get(
    "/quantity/active",
    summary="Отримати кількість активних контрактів"
)
async def get_active_contracts_quantity(
    service: InsuranceContractsService
):
    return await service.get_quantity_of_active_insurance_contracts()