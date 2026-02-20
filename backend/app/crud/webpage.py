from sqlalchemy.orm import Session
from typing import Optional, Dict
from datetime import datetime

from ..models import WebpageContent
from ..schemas import webpage as webpage_schemas
from ..services.webpage_fetcher import webpage_fetcher


def get_webpage_content(db: Session, webpage_id: int) -> Optional[WebpageContent]:
    return db.query(WebpageContent).filter(WebpageContent.id == webpage_id).first()


def get_webpage_content_by_knowledge(db: Session, knowledge_id: int) -> Optional[WebpageContent]:
    return db.query(WebpageContent).filter(
        WebpageContent.knowledge_item_id == knowledge_id
    ).first()


def create_webpage_content(
    db: Session, 
    knowledge_id: int, 
    webpage_data: Dict
) -> WebpageContent:
    db_webpage = WebpageContent(
        knowledge_item_id=knowledge_id,
        url=webpage_data.get("url"),
        title=webpage_data.get("title"),
        description=webpage_data.get("description"),
        summary=webpage_data.get("summary"),
        keywords=webpage_data.get("keywords"),
        fetched_at=datetime.utcnow()
    )
    db.add(db_webpage)
    db.commit()
    db.refresh(db_webpage)
    return db_webpage


def update_webpage_content(
    db: Session, 
    knowledge_id: int, 
    webpage_data: Dict
) -> Optional[WebpageContent]:
    db_webpage = get_webpage_content_by_knowledge(db, knowledge_id)
    if not db_webpage:
        return None
    
    # 更新字段
    update_data = {
        "url": webpage_data.get("url", db_webpage.url),
        "title": webpage_data.get("title", db_webpage.title),
        "description": webpage_data.get("description", db_webpage.description),
        "summary": webpage_data.get("summary", db_webpage.summary),
        "keywords": webpage_data.get("keywords", db_webpage.keywords),
        "fetched_at": datetime.utcnow()
    }
    
    for field, value in update_data.items():
        setattr(db_webpage, field, value)
    
    db.commit()
    db.refresh(db_webpage)
    return db_webpage


def delete_webpage_content(
    db: Session, 
    knowledge_id: int
) -> Optional[WebpageContent]:
    db_webpage = get_webpage_content_by_knowledge(db, knowledge_id)
    if not db_webpage:
        return None
    
    db.delete(db_webpage)
    db.commit()
    return db_webpage


def fetch_webpage(
    db: Session, 
    url: str
) -> Dict:
    # 抓取网页内容
    return webpage_fetcher.fetch(url)


def create_or_update_webpage_content(
    db: Session, 
    knowledge_id: int, 
    url: str
) -> Optional[WebpageContent]:
    # 抓取网页内容
    webpage_data = fetch_webpage(db, url)
    
    # 检查是否已存在
    existing_webpage = get_webpage_content_by_knowledge(db, knowledge_id)
    
    if existing_webpage:
        # 更新现有记录
        return update_webpage_content(db, knowledge_id, webpage_data)
    else:
        # 创建新记录
        return create_webpage_content(db, knowledge_id, webpage_data)
