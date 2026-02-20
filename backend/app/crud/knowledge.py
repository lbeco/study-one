from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from typing import Optional, List

from ..models import KnowledgeItem, Tag
from ..schemas import knowledge as knowledge_schemas


def get_knowledge_item(db: Session, item_id: int) -> Optional[KnowledgeItem]:
    return db.query(KnowledgeItem).options(
        joinedload(KnowledgeItem.tags),
        joinedload(KnowledgeItem.markdown_content),
        joinedload(KnowledgeItem.webpage_content)
    ).filter(KnowledgeItem.id == item_id).first()


def get_knowledge_items(
    db: Session, 
    page: int = 1, 
    page_size: int = 20,
    folder_id: Optional[int] = None,
    type: Optional[str] = None
) -> List[KnowledgeItem]:
    skip = (page - 1) * page_size
    query = db.query(KnowledgeItem)
    
    if folder_id is not None:
        query = query.filter(KnowledgeItem.folder_id == folder_id)
    
    if type is not None:
        query = query.filter(KnowledgeItem.type == type)
    
    return query.options(
        joinedload(KnowledgeItem.tags)
    ).offset(skip).limit(page_size).all()


def search_knowledge(
    db: Session, 
    query: str, 
    page: int = 1, 
    page_size: int = 20
) -> List[KnowledgeItem]:
    skip = (page - 1) * page_size
    search_term = f"%{query}%"
    
    # 搜索标题
    knowledge_query = db.query(KnowledgeItem).filter(
        KnowledgeItem.title.ilike(search_term)
    )
    
    # 搜索标签
    tag_ids = db.query(Tag.id).filter(Tag.name.ilike(search_term)).all()
    tag_ids = [tag[0] for tag in tag_ids]
    
    if tag_ids:
        knowledge_query = knowledge_query.filter(
            or_(
                KnowledgeItem.title.ilike(search_term),
                KnowledgeItem.tags.any(Tag.id.in_(tag_ids))
            )
        )
    
    return knowledge_query.options(
        joinedload(KnowledgeItem.tags)
    ).offset(skip).limit(page_size).all()


def create_knowledge_item(
    db: Session, 
    knowledge_item: knowledge_schemas.KnowledgeItemCreate
) -> KnowledgeItem:
    db_knowledge = KnowledgeItem(
        title=knowledge_item.title,
        type=knowledge_item.type,
        folder_id=knowledge_item.folder_id
    )
    db.add(db_knowledge)
    db.commit()
    db.refresh(db_knowledge)
    return db_knowledge


def update_knowledge_item(
    db: Session, 
    item_id: int, 
    knowledge_item: knowledge_schemas.KnowledgeItemUpdate
) -> Optional[KnowledgeItem]:
    db_knowledge = get_knowledge_item(db, item_id)
    if not db_knowledge:
        return None
    
    update_data = knowledge_item.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_knowledge, field, value)
    
    db.commit()
    db.refresh(db_knowledge)
    return db_knowledge


def delete_knowledge_item(db: Session, item_id: int) -> Optional[KnowledgeItem]:
    db_knowledge = get_knowledge_item(db, item_id)
    if not db_knowledge:
        return None
    
    db.delete(db_knowledge)
    db.commit()
    return db_knowledge


def add_tag_to_knowledge(
    db: Session, 
    knowledge_id: int, 
    tag_id: int
) -> Optional[KnowledgeItem]:
    db_knowledge = get_knowledge_item(db, knowledge_id)
    if not db_knowledge:
        return None
    
    db_tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not db_tag:
        return None
    
    if db_tag not in db_knowledge.tags:
        db_knowledge.tags.append(db_tag)
        db.commit()
        db.refresh(db_knowledge)
    
    return db_knowledge


def remove_tag_from_knowledge(
    db: Session, 
    knowledge_id: int, 
    tag_id: int
) -> Optional[KnowledgeItem]:
    db_knowledge = get_knowledge_item(db, knowledge_id)
    if not db_knowledge:
        return None
    
    db_tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not db_tag:
        return None
    
    if db_tag in db_knowledge.tags:
        db_knowledge.tags.remove(db_tag)
        db.commit()
        db.refresh(db_knowledge)
    
    return db_knowledge


def get_knowledge_by_tags(
    db: Session, 
    tag_ids: List[int], 
    page: int = 1, 
    page_size: int = 20
) -> List[KnowledgeItem]:
    skip = (page - 1) * page_size
    
    query = db.query(KnowledgeItem)
    for tag_id in tag_ids:
        query = query.filter(KnowledgeItem.tags.any(Tag.id == tag_id))
    
    return query.options(
        joinedload(KnowledgeItem.tags)
    ).offset(skip).limit(page_size).all()
