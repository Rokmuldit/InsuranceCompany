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

    def _build_insert_query(self, table: str, kwargs: dict) -> tuple[str, dict]:
        columns = ", ".join(kwargs.keys())
        placeholders = ", ".join(f":{k}" for k in kwargs.keys())
        query = f"INSERT INTO {table} ({columns}) OUTPUT INSERTED.ID VALUES ({placeholders})"
        return query, kwargs

    def _build_update_query(self, table: str, record_id: Any, kwargs: dict) -> tuple[str, dict]:
        set_clauses = ", ".join(f"{k} = :{k}" for k in kwargs.keys())
        query = f"UPDATE {table} SET {set_clauses} WHERE ID = :_id"
        params = {"_id": str(record_id), **kwargs}
        return query, params

    def _build_delete_query(self, table: str, record_id: Any) -> tuple[str, dict]:
        query = f"DELETE FROM {table} WHERE ID = :_id"
        return query, {"_id": str(record_id)}

    async def create_record(self, **kwargs) -> Any:
        if not self.table_name: raise ValueError("table_name is not defined")
        query, params = self._build_insert_query(self.table_name, kwargs)
        return await self._insert_and_return_id(query, params)

    async def update_record(self, record_id: Any, **kwargs) -> None:
        if not self.table_name: raise ValueError("table_name is not defined")
        query, params = self._build_update_query(self.table_name, record_id, kwargs)
        await self._execute_and_commit(query, params)

    async def delete_by_id(self, record_id: Any) -> None:
        if not self.table_name: raise ValueError("table_name is not defined")
        query, params = self._build_delete_query(self.table_name, record_id)
        await self._execute_and_commit(query, params)

    def _build_where(self, filters: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        if not filters: return "", {}
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

    async def count_all(self, base_query: str, filters: dict[str, Any] | None = None) -> int:
        where_clause, params = self._build_where(filters or {})
        count_query = f"SELECT COUNT(*) FROM ({base_query} {where_clause}) AS count_query"
        result = await self.session.execute(text(count_query), params)
        return int(result.scalar())

    async def find_paginated(
        self,
        base_query: str,
        page: int,
        size: int,
        filters: dict[str, Any] | None = None,
        order_by: str = "ID"
    ) -> list[dict]:
        where_clause, params = self._build_where(filters or {})
        offset = (page - 1) * size

        # MS SQL pagination
        query = (
            f"{base_query} {where_clause} "
            f"ORDER BY {order_by} "
            f"OFFSET {offset} ROWS FETCH NEXT {size} ROWS ONLY"
        )
        return await self._fetch_all(query, params)