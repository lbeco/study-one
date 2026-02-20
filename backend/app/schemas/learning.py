from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LearningRecordBase(BaseModel):
    question: str
    answer: Optional[str] = None
    is_correct: Optional[bool] = None


class LearningRecordCreate(LearningRecordBase):
    knowledge_item_id: int


class LearningRecord(LearningRecordBase):
    id: int
    knowledge_item_id: int
    created_at: datetime

    class Config:
        from_attributes = True
