from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from ...database import get_db
from ...crud import tag as tag_crud
from ...schemas import tag as tag_schemas
from ...schemas.common import ApiResponse

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("", response_model=ApiResponse[List[tag_schemas.Tag]])
async def get_tags(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    tags = tag_crud.get_tags(db, page=page, page_size=page_size)
    return ApiResponse(data=tags, message=f"获取到 {len(tags)} 个标签")


@router.get("/{tag_id}", response_model=ApiResponse[tag_schemas.Tag])
async def get_tag(
    tag_id: int,
    db: Session = Depends(get_db)
):
    tag = tag_crud.get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="标签不存在")
    return ApiResponse(data=tag, message="获取标签成功")


@router.post("", response_model=ApiResponse[tag_schemas.Tag])
async def create_tag(
    tag: tag_schemas.TagCreate,
    db: Session = Depends(get_db)
):
    db_tag = tag_crud.create_tag(db, tag)
    return ApiResponse(data=db_tag, message="创建标签成功")


@router.put("/{tag_id}", response_model=ApiResponse[tag_schemas.Tag])
async def update_tag(
    tag_id: int,
    tag: tag_schemas.TagUpdate,
    db: Session = Depends(get_db)
):
    db_tag = tag_crud.update_tag(db, tag_id, tag)
    if not db_tag:
        raise HTTPException(status_code=404, detail="标签不存在")
    return ApiResponse(data=db_tag, message="更新标签成功")


@router.delete("/{tag_id}", response_model=ApiResponse[tag_schemas.Tag])
async def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db)
):
    db_tag = tag_crud.delete_tag(db, tag_id)
    if not db_tag:
        raise HTTPException(status_code=404, detail="标签不存在")
    return ApiResponse(data=db_tag, message="删除标签成功")
