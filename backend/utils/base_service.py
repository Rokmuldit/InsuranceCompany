import math
from typing import TypeVar, Generic, Type, Any
from fastapi import HTTPException, status
from pydantic import BaseModel
from utils.pagination import Page

TResponse = TypeVar("TResponse", bound=BaseModel)

class BaseService(Generic[TResponse]):
    response_schema: Type[TResponse]

    def __init__(self, repo: Any):
        self.repo = repo

    async def _get_or_raise(
        self,
        fetch_coro: Any,
        detail: str = "Запис не знайдено.",
        status_code: int = status.HTTP_404_NOT_FOUND
    ) -> dict:
        result = await fetch_coro
        if not result:
            raise HTTPException(status_code=status_code, detail=detail)
        return result

    def _map_list(self, data_list: list[dict]) -> list[TResponse]:
        return [self.response_schema(**item) for item in data_list]

    async def get_paginated(
        self,
        page: int,
        size: int,
        base_query: str,
        filters: dict[str, Any] | None = None,
        order_by: str = "ID"
    ) -> Page[TResponse]:
        total = await self.repo.count_all(base_query, filters)
        items_data = await self.repo.find_paginated(base_query, page, size, filters, order_by)

        pages = math.ceil(total / size) if total > 0 else 0

        return Page(
            items=self._map_list(items_data),
            total=total,
            page=page,
            size=size,
            pages=pages
        )