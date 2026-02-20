from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class KnowledgeItemBase(BaseModel):
    title: str
    type: str
    folder_id: Optional[int] = None


class KnowledgeItemCreate(KnowledgeItemBase):
    pass


class KnowledgeItemUpdate(BaseModel):
    title: Optional[str] = None
    folder_id: Optional[int] = None


class KnowledgeItem(KnowledgeItemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class KnowledgeItemDetail(KnowledgeItem):
    tags: List["Tag"] = []
    markdown_content: Optional["MarkdownContent"] = None
    webpage_content: Optional["WebpageContent"] = None


from .tag import Tag
from .markdown import MarkdownContent
from .webpage import WebpageContent
KnowledgeItemDetail.model_rebuild()
