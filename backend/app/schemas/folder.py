from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class FolderBase(BaseModel):
    name: str
    parent_id: Optional[int] = None


class FolderCreate(FolderBase):
    pass


class FolderUpdate(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[int] = None


class Folder(FolderBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class FolderWithChildren(Folder):
    children: List["FolderWithChildren"] = []


FolderWithChildren.model_rebuild()
