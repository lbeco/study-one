from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class KnowledgeItem(Base):
    __tablename__ = "knowledge_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)
    folder_id = Column(Integer, ForeignKey("folders.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    folder = relationship("Folder", back_populates="knowledge_items")
    tags = relationship("Tag", secondary="knowledge_tags", back_populates="knowledge_items")
    markdown_content = relationship("MarkdownContent", back_populates="knowledge_item", uselist=False)
    webpage_content = relationship("WebpageContent", back_populates="knowledge_item", uselist=False)
    learning_records = relationship("LearningRecord", back_populates="knowledge_item")
