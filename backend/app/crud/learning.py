from sqlalchemy.orm import Session
from typing import Optional, List

from ..models import LearningRecord
from ..schemas import learning as learning_schemas


def get_learning_record(db: Session, record_id: int) -> Optional[LearningRecord]:
    return db.query(LearningRecord).filter(LearningRecord.id == record_id).first()


def get_learning_records_by_knowledge(
    db: Session, 
    knowledge_id: int,
    page: int = 1,
    page_size: int = 20
) -> List[LearningRecord]:
    skip = (page - 1) * page_size
    return db.query(LearningRecord).filter(
        LearningRecord.knowledge_item_id == knowledge_id
    ).offset(skip).limit(page_size).all()


def create_learning_record(
    db: Session, 
    knowledge_id: int,
    question: str,
    answer: Optional[str] = None,
    is_correct: Optional[bool] = None
) -> LearningRecord:
    db_record = LearningRecord(
        knowledge_item_id=knowledge_id,
        question=question,
        answer=answer,
        is_correct=is_correct
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def delete_learning_record(db: Session, record_id: int) -> Optional[LearningRecord]:
    db_record = get_learning_record(db, record_id)
    if not db_record:
        return None
    
    db.delete(db_record)
    db.commit()
    return db_record
