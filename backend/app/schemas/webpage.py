from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime


class WebpageContentBase(BaseModel):
    url: str
    title: Optional[str] = None
    description: Optional[str] = None
    summary: Optional[str] = None
    keywords: Optional[str] = None


class WebpageContentCreate(WebpageContentBase):
    pass


class WebpageContentUpdate(BaseModel):
    url: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    summary: Optional[str] = None
    keywords: Optional[str] = None


class WebpageContent(WebpageContentBase):
    id: int
    knowledge_item_id: int
    fetched_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class WebpageFetchRequest(BaseModel):
    url: str
