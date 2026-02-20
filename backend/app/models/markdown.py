from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class MarkdownContent(Base):
    __tablename__ = "markdown_contents"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    knowledge_item_id = Column(Integer, ForeignKey("knowledge_items.id", ondelete="CASCADE"), nullable=False)
    file_path = Column(String(500), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    knowledge_item = relationship("KnowledgeItem", back_populates="markdown_content")
