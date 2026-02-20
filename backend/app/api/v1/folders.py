from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ...database import get_db
from ...crud import folder as folder_crud
from ...schemas import folder as folder_schemas
from ...schemas.common import ApiResponse

router = APIRouter(prefix="/folders", tags=["folders"])


@router.get("", response_model=ApiResponse[List[folder_schemas.Folder]])
async def get_folders(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    folders = folder_crud.get_folders(db, page=page, page_size=page_size)
    return ApiResponse(data=folders, message=f"获取到 {len(folders)} 个文件夹")


@router.get("/tree", response_model=ApiResponse[List[folder_schemas.FolderWithChildren]])
async def get_folder_tree(
    root_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    folder_tree = folder_crud.get_folder_tree(db, root_id=root_id)
    return ApiResponse(data=folder_tree, message="获取文件夹树成功")


@router.get("/parent/{parent_id}", response_model=ApiResponse[List[folder_schemas.Folder]])
async def get_folders_by_parent(
    parent_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    folders = folder_crud.get_folders_by_parent(db, parent_id=parent_id)
    return ApiResponse(data=folders, message=f"获取到 {len(folders)} 个文件夹")


@router.get("/{folder_id}", response_model=ApiResponse[folder_schemas.Folder])
async def get_folder(
    folder_id: int,
    db: Session = Depends(get_db)
):
    folder = folder_crud.get_folder(db, folder_id)
    if not folder:
        raise HTTPException(status_code=404, detail="文件夹不存在")
    return ApiResponse(data=folder, message="获取文件夹成功")


@router.post("", response_model=ApiResponse[folder_schemas.Folder])
async def create_folder(
    folder: folder_schemas.FolderCreate,
    db: Session = Depends(get_db)
):
    db_folder = folder_crud.create_folder(db, folder)
    return ApiResponse(data=db_folder, message="创建文件夹成功")


@router.put("/{folder_id}", response_model=ApiResponse[folder_schemas.Folder])
async def update_folder(
    folder_id: int,
    folder: folder_schemas.FolderUpdate,
    db: Session = Depends(get_db)
):
    db_folder = folder_crud.update_folder(db, folder_id, folder)
    if not db_folder:
        raise HTTPException(status_code=404, detail="文件夹不存在")
    return ApiResponse(data=db_folder, message="更新文件夹成功")


@router.delete("/{folder_id}", response_model=ApiResponse[folder_schemas.Folder])
async def delete_folder(
    folder_id: int,
    db: Session = Depends(get_db)
):
    db_folder = folder_crud.delete_folder(db, folder_id)
    if not db_folder:
        raise HTTPException(status_code=404, detail="文件夹不存在")
    return ApiResponse(data=db_folder, message="删除文件夹成功")
