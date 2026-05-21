import uuid
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from utils.base_repo import BaseRepo


class PersonalDataRepo(BaseRepo):
    table_name = "PersonalData"
    _BASE_QUERY = """
                  SELECT PD.ID          AS id, \
                         PD.FirstName   AS first_name, \
                         PD.LastName    AS last_name, \
                         PD.MiddleName  AS middle_name, \
                         PD.BirthDate   AS birth_date, \
                         PD.PhoneNumber AS phone_number, \
                         A.ID           AS address_id, \
                         A.Region       AS region, \
                         A.City         AS city, \
                         A.Street       AS street, \
                         A.House        AS house, \
                         A.Apartment    AS apartment                  
                  FROM PersonalData PD                           
                           INNER JOIN Address A ON PD.ID_Address = A.ID \
                  """

    async def create_full(self, pd_data: dict, address_data: dict) -> uuid.UUID:
        addr_q, addr_p = self._build_insert_query("Address", address_data)
        address_id = (await self.session.execute(text(addr_q), addr_p)).scalar()

        pd_data["ID_Address"] = address_id
        pd_q, pd_p = self._build_insert_query(self.table_name, pd_data)
        new_pd_id = (await self.session.execute(text(pd_q), pd_p)).scalar()

        await self.session.commit()
        return new_pd_id

    async def update_full(self, pd_id: uuid.UUID, pd_data: dict, address_data: dict) -> None:
        addr_id_q = "SELECT ID_Address FROM PersonalData WHERE ID = :id"
        address_id = (await self.session.execute(text(addr_id_q), {"id": str(pd_id)})).scalar()

        if address_data and address_id:
            addr_q, addr_p = self._build_update_query("Address", address_id, address_data)
            await self.session.execute(text(addr_q), addr_p)

        if pd_data:
            pd_q, pd_p = self._build_update_query(self.table_name, pd_id, pd_data)
            await self.session.execute(text(pd_q), pd_p)

        await self.session.commit()

    async def delete_full(self, pd_id: uuid.UUID) -> None:
        addr_id_q = "SELECT ID_Address FROM PersonalData WHERE ID = :id"
        address_id = (await self.session.execute(text(addr_id_q), {"id": str(pd_id)})).scalar()

        pd_q, pd_p = self._build_delete_query(self.table_name, pd_id)
        await self.session.execute(text(pd_q), pd_p)

        if address_id:
            addr_q, addr_p = self._build_delete_query("Address", address_id)
            await self.session.execute(text(addr_q), addr_p)

        await self.session.commit()

    async def get_all(self) -> list[dict]:
        return await self.find_all(self._BASE_QUERY)

    async def get_by_id(self, pd_id: uuid.UUID) -> dict | None:
        return await self.find_one(self._BASE_QUERY, {"PD.ID": str(pd_id)})

    async def get_by_client_id(self, client_id: uuid.UUID) -> dict | None:
        query = self._BASE_QUERY + " INNER JOIN Client C ON C.ID_PersonalData = PD.ID"
        return await self.find_one(query, {"C.ID": str(client_id)})