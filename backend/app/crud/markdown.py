from sqlalchemy.orm import Session
from typing import Optional

from ..models import MarkdownContent, KnowledgeItem
from ..schemas import markdown as markdown_schemas
from ..services.file_service import file_service


def get_markdown_content(db: Session, markdown_id: int) -> Optional[MarkdownContent]:
    return db.query(MarkdownContent).filter(MarkdownContent.id == markdown_id).first()


def get_markdown_content_by_knowledge(db: Session, knowledge_id: int) -> Optional[MarkdownContent]:
    return db.query(MarkdownContent).filter(
        MarkdownContent.knowledge_item_id == knowledge_id
    ).first()


def create_markdown_content(
    db: Session, 
    knowledge_id: int, 
    content: str
) -> MarkdownContent:
    # 保存到文件系统
    file_path = file_service.save_markdown(content)
    
    # 创建数据库记录
    db_markdown = MarkdownContent(
        knowledge_item_id=knowledge_id,
        file_path=file_path
    )
    db.add(db_markdown)
    db.commit()
    db.refresh(db_markdown)
    return db_markdown


def update_markdown_content(
    db: Session, 
    knowledge_id: int, 
    content: str
) -> Optional[MarkdownContent]:
    db_markdown = get_markdown_content_by_knowledge(db, knowledge_id)
    if not db_markdown:
        return None
    
    # 更新文件内容
    file_service.update_markdown(db_markdown.file_path, content)
    
    # 不需要更新数据库记录，因为只更新了文件内容
    db.commit()
    return db_markdown


def delete_markdown_content(
    db: Session, 
    knowledge_id: int
) -> Optional[MarkdownContent]:
    db_markdown = get_markdown_content_by_knowledge(db, knowledge_id)
    if not db_markdown:
        return None
    
    # 删除文件
    file_service.delete_file(db_markdown.file_path)
    
    # 删除数据库记录
    db.delete(db_markdown)
    db.commit()
    return db_markdown


def get_markdown_content_with_data(
    db: Session, 
    knowledge_id: int
) -> Optional[markdown_schemas.MarkdownContentWithData]:
    db_markdown = get_markdown_content_by_knowledge(db, knowledge_id)
    if not db_markdown:
        return None
    
    # 读取文件内容
    content = file_service.read_markdown(db_markdown.file_path)
    
    # 构建响应
    return markdown_schemas.MarkdownContentWithData(
        id=db_markdown.id,
        knowledge_item_id=db_markdown.knowledge_item_id,
        file_path=db_markdown.file_path,
        created_at=db_markdown.created_at,
        updated_at=db_markdown.updated_at,
        content=content
    )
