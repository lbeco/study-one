from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MarkdownContentBase(BaseModel):
    file_path: str


class MarkdownContentCreate(MarkdownContentBase):
    pass


class MarkdownContentUpdate(BaseModel):
    file_path: Optional[str] = None


class MarkdownContent(MarkdownContentBase):
    id: int
    knowledge_item_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MarkdownContentWithData(MarkdownContent):
    content: Optional[str] = None
