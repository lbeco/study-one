from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class WebpageContent(Base):
    __tablename__ = "webpage_contents"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    knowledge_item_id = Column(Integer, ForeignKey("knowledge_items.id", ondelete="CASCADE"), nullable=False)
    url = Column(String(1000), nullable=False)
    title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    keywords = Column(Text, nullable=True)
    fetched_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    knowledge_item = relationship("KnowledgeItem", back_populates="webpage_content")
