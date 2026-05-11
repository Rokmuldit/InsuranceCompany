from typing import Any
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepo:
    table_name: str | None = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def _fetch_one(self, query: str, params: dict[str, Any] | None = None) -> dict | None:
        result = await self.session.execute(text(query), params or {})
        row = result.mappings().first()
        return dict(row) if row else None

    async def _fetch_all(self, query: str, params: dict[str, Any] | None = None) -> list[dict]:
        result = await self.session.execute(text(query), params or {})
        return [dict(row) for row in result.mappings().all()]

    async def _execute_and_commit(self, query: str, params: dict[str, Any] | None = None) -> None:
        await self.session.execute(text(query), params or {})
        await self.session.commit()

    async def _insert_and_return_id(self, query: str, params: dict[str, Any] | None = None) -> Any:
        result = await self.session.execute(text(query), params or {})
        await self.session.commit()
        return result.scalar()

    # ---

    async def create_record(self, **kwargs) -> Any:
        if not self.table_name:
            raise ValueError("table_name is not defined")

        columns = ", ".join(kwargs.keys())
        placeholders = ", ".join(f":{k}" for k in kwargs.keys())

        query = f"""
            INSERT INTO {self.table_name} ({columns}) 
            OUTPUT INSERTED.ID 
            VALUES ({placeholders})
        """
        return await self._insert_and_return_id(query, kwargs)

    async def update_record(self, record_id: Any, **kwargs) -> None:
        if not self.table_name:
            raise ValueError("table_name is not defined")

        set_clauses = ", ".join(f"{k} = :{k}" for k in kwargs.keys())
        query = f"UPDATE {self.table_name} SET {set_clauses} WHERE ID = :id"

        params = {"id": str(record_id), **kwargs}
        await self._execute_and_commit(query, params)

    async def delete_by_id(self, record_id: Any) -> None:
        if not self.table_name:
            raise ValueError("table_name is not defined")

        query = f"DELETE FROM {self.table_name} WHERE ID = :id"
        await self._execute_and_commit(query, {"id": str(record_id)})

    # ---

    def _build_where(self, filters: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        """
        {"IC.ID": 123} -> (" WHERE IC.ID = :p_0", {"p_0": 123})
        """
        if not filters:
            return "", {}

        clauses = []
        params = {}
        for i, (column, value) in enumerate(filters.items()):
            param_name = f"p_{i}"
            clauses.append(f"{column} = :{param_name}")
            params[param_name] = value

        return " WHERE " + " AND ".join(clauses), params

    async def find_all(self, base_query: str, filters: dict[str, Any] | None = None) -> list[dict]:
        where_clause, params = self._build_where(filters or {})
        query = base_query + where_clause
        return await self._fetch_all(query, params)

    async def find_one(self, base_query: str, filters: dict[str, Any] | None = None) -> dict | None:
        where_clause, params = self._build_where(filters or {})
        query = base_query + where_clause
        return await self._fetch_one(query, params)