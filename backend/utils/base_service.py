from typing import TypeVar, Generic, Type, Any
from fastapi import HTTPException, status
from pydantic import BaseModel

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