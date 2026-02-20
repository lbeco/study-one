from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ...database import get_db
from ...crud import knowledge as knowledge_crud
from ...schemas import knowledge as knowledge_schemas
from ...schemas.common import ApiResponse

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


@router.get("", response_model=ApiResponse[List[knowledge_schemas.KnowledgeItem]])
async def get_knowledge_items(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    folder_id: Optional[int] = None,
    type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    knowledge_items = knowledge_crud.get_knowledge_items(
        db, 
        page=page, 
        page_size=page_size,
        folder_id=folder_id,
        type=type
    )
    return ApiResponse(data=knowledge_items, message=f"获取到 {len(knowledge_items)} 个知识项")


@router.get("/search", response_model=ApiResponse[List[knowledge_schemas.KnowledgeItem]])
async def search_knowledge(
    q: str = Query(..., description="搜索关键词"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    knowledge_items = knowledge_crud.search_knowledge(
        db, 
        query=q, 
        page=page, 
        page_size=page_size
    )
    return ApiResponse(data=knowledge_items, message=f"搜索到 {len(knowledge_items)} 个知识项")


@router.get("/by-tags", response_model=ApiResponse[List[knowledge_schemas.KnowledgeItem]])
async def get_knowledge_by_tags(
    tag_ids: str = Query(..., description="标签ID，多个用逗号分隔"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    try:
        tag_id_list = [int(tag_id) for tag_id in tag_ids.split(",")]
    except ValueError:
        raise HTTPException(status_code=400, detail="标签ID格式错误")
    
    knowledge_items = knowledge_crud.get_knowledge_by_tags(
        db, 
        tag_ids=tag_id_list, 
        page=page, 
        page_size=page_size
    )
    return ApiResponse(data=knowledge_items, message=f"获取到 {len(knowledge_items)} 个知识项")


@router.get("/{item_id}", response_model=ApiResponse[knowledge_schemas.KnowledgeItem])
async def get_knowledge_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    knowledge_item = knowledge_crud.get_knowledge_item(db, item_id)
    if not knowledge_item:
        raise HTTPException(status_code=404, detail="知识项不存在")
    return ApiResponse(data=knowledge_item, message="获取知识项成功")


@router.post("", response_model=ApiResponse[knowledge_schemas.KnowledgeItem])
async def create_knowledge_item(
    knowledge_item: knowledge_schemas.KnowledgeItemCreate,
    db: Session = Depends(get_db)
):
    db_knowledge = knowledge_crud.create_knowledge_item(db, knowledge_item)
    return ApiResponse(data=db_knowledge, message="创建知识项成功")


@router.put("/{item_id}", response_model=ApiResponse[knowledge_schemas.KnowledgeItem])
async def update_knowledge_item(
    item_id: int,
    knowledge_item: knowledge_schemas.KnowledgeItemUpdate,
    db: Session = Depends(get_db)
):
    db_knowledge = knowledge_crud.update_knowledge_item(db, item_id, knowledge_item)
    if not db_knowledge:
        raise HTTPException(status_code=404, detail="知识项不存在")
    return ApiResponse(data=db_knowledge, message="更新知识项成功")


@router.delete("/{item_id}", response_model=ApiResponse[knowledge_schemas.KnowledgeItem])
async def delete_knowledge_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    db_knowledge = knowledge_crud.delete_knowledge_item(db, item_id)
    if not db_knowledge:
        raise HTTPException(status_code=404, detail="知识项不存在")
    return ApiResponse(data=db_knowledge, message="删除知识项成功")


@router.post("/{item_id}/tags/{tag_id}", response_model=ApiResponse[knowledge_schemas.KnowledgeItem])
async def add_tag_to_knowledge(
    item_id: int,
    tag_id: int,
    db: Session = Depends(get_db)
):
    db_knowledge = knowledge_crud.add_tag_to_knowledge(db, item_id, tag_id)
    if not db_knowledge:
        raise HTTPException(status_code=404, detail="知识项或标签不存在")
    return ApiResponse(data=db_knowledge, message="添加标签成功")


@router.delete("/{item_id}/tags/{tag_id}", response_model=ApiResponse[knowledge_schemas.KnowledgeItem])
async def remove_tag_from_knowledge(
    item_id: int,
    tag_id: int,
    db: Session = Depends(get_db)
):
    db_knowledge = knowledge_crud.remove_tag_from_knowledge(db, item_id, tag_id)
    if not db_knowledge:
        raise HTTPException(status_code=404, detail="知识项或标签不存在")
    return ApiResponse(data=db_knowledge, message="移除标签成功")
