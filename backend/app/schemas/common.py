from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool = True
    data: Optional[T] = None
    message: str = "操作成功"


class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 20
