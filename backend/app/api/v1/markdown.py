from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel

from ...database import get_db
from ...crud import markdown as markdown_crud
from ...crud import knowledge as knowledge_crud
from ...schemas import markdown as markdown_schemas
from ...schemas.common import ApiResponse

router = APIRouter(prefix="/knowledge", tags=["markdown"])


class MarkdownContentUpdate(BaseModel):
    content: str


@router.get("/{item_id}/markdown", response_model=ApiResponse[markdown_schemas.MarkdownContentWithData])
async def get_markdown_content(
    item_id: int,
    db: Session = Depends(get_db)
):
    # 检查知识项是否存在
    knowledge_item = knowledge_crud.get_knowledge_item(db, item_id)
    if not knowledge_item:
        raise HTTPException(status_code=404, detail="知识项不存在")
    
    markdown_content = markdown_crud.get_markdown_content_with_data(db, item_id)
    if not markdown_content:
        raise HTTPException(status_code=404, detail="Markdown 内容不存在")
    
    return ApiResponse(data=markdown_content, message="获取 Markdown 内容成功")


@router.put("/{item_id}/markdown", response_model=ApiResponse[markdown_schemas.MarkdownContent])
async def update_markdown_content(
    item_id: int,
    markdown_data: MarkdownContentUpdate,
    db: Session = Depends(get_db)
):
    # 检查知识项是否存在
    knowledge_item = knowledge_crud.get_knowledge_item(db, item_id)
    if not knowledge_item:
        raise HTTPException(status_code=404, detail="知识项不存在")
    
    # 检查是否为 Markdown 类型
    if knowledge_item.type != "markdown":
        raise HTTPException(status_code=400, detail="该知识项不是 Markdown 类型")
    
    # 检查是否已有 Markdown 内容
    existing_content = markdown_crud.get_markdown_content_by_knowledge(db, item_id)
    if existing_content:
        # 更新现有内容
        markdown_content = markdown_crud.update_markdown_content(db, item_id, markdown_data.content)
    else:
        # 创建新内容
        markdown_content = markdown_crud.create_markdown_content(db, item_id, markdown_data.content)
    
    return ApiResponse(data=markdown_content, message="更新 Markdown 内容成功")


@router.post("/markdown/upload", response_model=ApiResponse[markdown_schemas.MarkdownContent])
async def upload_markdown_file(
    item_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 检查知识项是否存在
    knowledge_item = knowledge_crud.get_knowledge_item(db, item_id)
    if not knowledge_item:
        raise HTTPException(status_code=404, detail="知识项不存在")
    
    # 检查是否为 Markdown 类型
    if knowledge_item.type != "markdown":
        raise HTTPException(status_code=400, detail="该知识项不是 Markdown 类型")
    
    # 读取文件内容
    content = await file.read()
    content = content.decode("utf-8")
    
    # 检查是否已有 Markdown 内容
    existing_content = markdown_crud.get_markdown_content_by_knowledge(db, item_id)
    if existing_content:
        # 更新现有内容
        markdown_content = markdown_crud.update_markdown_content(db, item_id, content)
    else:
        # 创建新内容
        markdown_content = markdown_crud.create_markdown_content(db, item_id, content)
    
    return ApiResponse(data=markdown_content, message="上传 Markdown 文件成功")
