from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict
from pydantic import BaseModel

from ...database import get_db
from ...crud import webpage as webpage_crud
from ...crud import knowledge as knowledge_crud
from ...schemas import webpage as webpage_schemas
from ...schemas.common import ApiResponse

router = APIRouter(prefix="/knowledge", tags=["webpage"])


@router.get("/{item_id}/webpage", response_model=ApiResponse[webpage_schemas.WebpageContent])
async def get_webpage_content(
    item_id: int,
    db: Session = Depends(get_db)
):
    # 检查知识项是否存在
    knowledge_item = knowledge_crud.get_knowledge_item(db, item_id)
    if not knowledge_item:
        raise HTTPException(status_code=404, detail="知识项不存在")
    
    webpage_content = webpage_crud.get_webpage_content_by_knowledge(db, item_id)
    if not webpage_content:
        raise HTTPException(status_code=404, detail="网页内容不存在")
    
    return ApiResponse(data=webpage_content, message="获取网页内容成功")


@router.post("/{item_id}/webpage", response_model=ApiResponse[webpage_schemas.WebpageContent])
async def create_webpage_content(
    item_id: int,
    webpage_data: webpage_schemas.WebpageContentCreate,
    db: Session = Depends(get_db)
):
    # 检查知识项是否存在
    knowledge_item = knowledge_crud.get_knowledge_item(db, item_id)
    if not knowledge_item:
        raise HTTPException(status_code=404, detail="知识项不存在")
    
    # 检查是否为网页类型
    if knowledge_item.type != "webpage":
        raise HTTPException(status_code=400, detail="该知识项不是网页类型")
    
    # 检查是否已有网页内容
    existing_content = webpage_crud.get_webpage_content_by_knowledge(db, item_id)
    if existing_content:
        # 更新现有内容
        webpage_content = webpage_crud.update_webpage_content(db, item_id, {
            "url": webpage_data.url,
            "title": webpage_data.title,
            "description": webpage_data.description,
            "summary": webpage_data.summary,
            "keywords": webpage_data.keywords
        })
    else:
        # 创建新内容
        webpage_content = webpage_crud.create_webpage_content(db, item_id, {
            "url": webpage_data.url,
            "title": webpage_data.title,
            "description": webpage_data.description,
            "summary": webpage_data.summary,
            "keywords": webpage_data.keywords
        })
    
    return ApiResponse(data=webpage_content, message="创建/更新网页内容成功")


@router.post("/webpage/fetch", response_model=ApiResponse[Dict])
async def fetch_webpage(
    fetch_request: webpage_schemas.WebpageFetchRequest,
    db: Session = Depends(get_db)
):
    # 抓取网页内容
    webpage_data = webpage_crud.fetch_webpage(db, fetch_request.url)
    
    if "error" in webpage_data:
        return ApiResponse(
            success=False,
            data=webpage_data,
            message=f"抓取网页失败: {webpage_data['error']}"
        )
    
    return ApiResponse(data=webpage_data, message="抓取网页成功")


class WebpageFetchUpdate(BaseModel):
    url: str


@router.post("/{item_id}/webpage/fetch", response_model=ApiResponse[webpage_schemas.WebpageContent])
async def fetch_and_update_webpage(
    item_id: int,
    fetch_data: WebpageFetchUpdate,
    db: Session = Depends(get_db)
):
    # 检查知识项是否存在
    knowledge_item = knowledge_crud.get_knowledge_item(db, item_id)
    if not knowledge_item:
        raise HTTPException(status_code=404, detail="知识项不存在")
    
    # 检查是否为网页类型
    if knowledge_item.type != "webpage":
        raise HTTPException(status_code=400, detail="该知识项不是网页类型")
    
    # 抓取网页并更新内容
    webpage_content = webpage_crud.create_or_update_webpage_content(db, item_id, fetch_data.url)
    
    if not webpage_content:
        raise HTTPException(status_code=500, detail="抓取网页失败")
    
    return ApiResponse(data=webpage_content, message="抓取并更新网页内容成功")
