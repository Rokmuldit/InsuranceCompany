import uuid
from datetime import date, timedelta
from decimal import Decimal
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from utils.base_repo import BaseRepo


class InsuranceContractsRepo(BaseRepo):
    table_name = "InsuranceContract"
    _BASE_GET_QUERY = """
                      SELECT IC.ID             AS contract_id, \
                             IC.ContractAmount AS contract_amount, \
                             IC.StartDate      AS start_date, \
                             IC.EndDate        AS end_date, \
                             IC.IsActive       AS is_active, \

                             C.ID              AS client_id, \
                             CPD.FirstName     AS client_first_name, \
                             CPD.LastName      AS client_last_name, \
                             CPD.MiddleName    AS client_middle_name, \
                             CPD.BirthDate     AS client_birth_date, \
                             CPD.PhoneNumber   AS client_phone_number, \
                             CA.Region         AS client_region, \
                             CA.City           AS client_city, \
                             CA.Street         AS client_street, \
                             CA.House          AS client_house, \
                             CA.Apartment      AS client_apartment, \

                             A.ID              AS agent_id, \
                             APD.FirstName     AS agent_first_name, \
                             APD.LastName      AS agent_last_name, \
                             APD.MiddleName    AS agent_middle_name, \
                             APD.BirthDate     AS agent_birth_date, \
                             APD.PhoneNumber   AS agent_phone_number, \
                             AA.Region         AS agent_region, \
                             AA.City           AS agent_city, \
                             AA.Street         AS agent_street, \
                             AA.House          AS agent_house, \
                             AA.Apartment      AS agent_apartment

                      FROM InsuranceContract IC
                               INNER JOIN Client C ON IC.ID_Client = C.ID
                               INNER JOIN PersonalData CPD ON C.ID_PersonalData = CPD.ID
                               INNER JOIN Address CA ON CPD.ID_Address = CA.ID

                               INNER JOIN Agent A ON IC.ID_Agent = A.ID
                               INNER JOIN Client AC ON A.ID_Client = AC.ID
                               INNER JOIN PersonalData APD ON AC.ID_PersonalData = APD.ID
                               INNER JOIN Address AA ON APD.ID_Address = AA.ID \
                      """

    async def create_insurance_contract(
            self, plan_id: uuid.UUID, client_id: uuid.UUID, agent_id: uuid.UUID
    ) -> uuid.UUID | str:

        plan_query = "SELECT PAYMENT_AMOUNT AS payment_amount, PAYMENT_PERIOD AS payment_period FROM PaidPlans"
        plan_data = await self.find_one(plan_query, {"ID": str(plan_id)})

        if not plan_data:
            raise ValueError("Plan not found")

        start_date = date.today()
        days_to_add = int(plan_data["payment_period"].lower())
        end_date = start_date + timedelta(days=days_to_add)

        return await self.create_record(
            ContractAmount=plan_data["payment_amount"],
            StartDate=start_date,
            EndDate=end_date,
            IsActive=1,
            ID_Client=str(client_id),
            ID_Agent=str(agent_id)
        )

    async def get_insurance_contract_by_id(self, contract_id: uuid.UUID) -> dict | None:
        return await self.find_one(self._BASE_GET_QUERY, {"IC.ID": str(contract_id)})

    async def get_insurance_contracts_by_client_id(self, client_id: uuid.UUID) -> list[dict]:
        return await self.find_all(self._BASE_GET_QUERY, {"IC.ID_Client": str(client_id)})

    async def get_insurance_contracts_by_agent_id(self, agent_id: uuid.UUID) -> list[dict]:
        return await self.find_all(self._BASE_GET_QUERY, {"IC.ID_Agent": str(agent_id)})

    async def get_insurance_contracts_by_plan_id(self, plan_id: uuid.UUID) -> list[dict]:
        plan_query = "SELECT PAYMENT_AMOUNT AS payment_amount FROM PaidPlans"
        plan_data = await self.find_one(plan_query, {"ID": str(plan_id)})

        if not plan_data:
            return []

        return await self.find_all(self._BASE_GET_QUERY, {"IC.ContractAmount": plan_data["payment_amount"]})

    async def get_all_insurance_contracts(self) -> list[dict]:
        return await self.find_all(self._BASE_GET_QUERY)

    async def get_all_not_active_insurance_contracts(self) -> list[dict]:
        return await self.find_all(self._BASE_GET_QUERY, {"IC.IsActive": 0})

    async def activate_insurance_contract(self, contract_id: uuid.UUID) -> None:
        await self.update_record(record_id=contract_id, IsActive=1)

    async def get_quantity_of_active_insurance_contracts(self) -> int:
        query = "SELECT COUNT(*) AS quantity FROM InsuranceContract WHERE IsActive = 1"
        result = await self.session.execute(text(query))
        return int(result.scalar())