from sqlalchemy.orm import Session
from typing import Optional, List

from ..models import Tag
from ..schemas import tag as tag_schemas


def get_tag(db: Session, tag_id: int) -> Optional[Tag]:
    return db.query(Tag).filter(Tag.id == tag_id).first()


def get_tag_by_name(db: Session, name: str) -> Optional[Tag]:
    return db.query(Tag).filter(Tag.name == name).first()


def get_tags(db: Session, page: int = 1, page_size: int = 20) -> List[Tag]:
    skip = (page - 1) * page_size
    return db.query(Tag).offset(skip).limit(page_size).all()


def create_tag(db: Session, tag: tag_schemas.TagCreate) -> Tag:
    # 检查标签是否已存在
    existing_tag = get_tag_by_name(db, tag.name)
    if existing_tag:
        return existing_tag
    
    db_tag = Tag(
        name=tag.name,
        color=tag.color
    )
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def update_tag(db: Session, tag_id: int, tag: tag_schemas.TagUpdate) -> Optional[Tag]:
    db_tag = get_tag(db, tag_id)
    if not db_tag:
        return None
    
    update_data = tag.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_tag, field, value)
    
    db.commit()
    db.refresh(db_tag)
    return db_tag


def delete_tag(db: Session, tag_id: int) -> Optional[Tag]:
    db_tag = get_tag(db, tag_id)
    if not db_tag:
        return None
    
    db.delete(db_tag)
    db.commit()
    return db_tag
