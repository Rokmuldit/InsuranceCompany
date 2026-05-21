import uuid
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from utils.base_repo import BaseRepo


class ClientRepo(BaseRepo):
    table_name = "Client"
    _BASE_QUERY = """
                  SELECT C.ID           AS id, \
                         PD.ID          AS personal_data_id, \
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
                  FROM Client C
                           INNER JOIN PersonalData PD ON C.ID_PersonalData = PD.ID
                           INNER JOIN Address A ON PD.ID_Address = A.ID \
                  """

    async def create_client(self, personal_data_id: uuid.UUID) -> uuid.UUID:
        return await self.create_record(ID_PersonalData=str(personal_data_id))

    async def get_all(self) -> list[dict]:
        return await self.find_all(self._BASE_QUERY)

    async def get_by_id(self, client_id: uuid.UUID) -> dict | None:
        return await self.find_one(self._BASE_QUERY, {"C.ID": str(client_id)})

    async def search_complex(self, filters: dict) -> list[dict]:
        if not filters:
            return await self.get_all()

        clauses = []
        params = {}
        for i, (column, value) in enumerate(filters.items()):
            param_name = f"p_{i}"
            if isinstance(value, str):
                clauses.append(f"{column} LIKE :{param_name}")
                params[param_name] = f"%{value}%"
            else:
                clauses.append(f"{column} = :{param_name}")
                params[param_name] = value

        where_clause = " WHERE " + " AND ".join(clauses)
        query = self._BASE_QUERY + where_clause

        result = await self.session.execute(text(query), params)
        return [dict(row) for row in result.mappings().all()]

    async def get_sum_of_all_clients(self) -> int:
        query = "SELECT COUNT(*) FROM Client"
        result = await self.session.execute(text(query))
        return int(result.scalar())