from sqlalchemy.orm import Session
from typing import Optional, List

from ..models import Folder
from ..schemas import folder as folder_schemas


def get_folder(db: Session, folder_id: int) -> Optional[Folder]:
    return db.query(Folder).filter(Folder.id == folder_id).first()


def get_folders(db: Session, page: int = 1, page_size: int = 20) -> List[Folder]:
    skip = (page - 1) * page_size
    return db.query(Folder).offset(skip).limit(page_size).all()


def get_folders_by_parent(db: Session, parent_id: Optional[int] = None) -> List[Folder]:
    return db.query(Folder).filter(Folder.parent_id == parent_id).all()


def create_folder(db: Session, folder: folder_schemas.FolderCreate) -> Folder:
    db_folder = Folder(
        name=folder.name,
        parent_id=folder.parent_id
    )
    db.add(db_folder)
    db.commit()
    db.refresh(db_folder)
    return db_folder


def update_folder(db: Session, folder_id: int, folder: folder_schemas.FolderUpdate) -> Optional[Folder]:
    db_folder = get_folder(db, folder_id)
    if not db_folder:
        return None
    
    update_data = folder.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_folder, field, value)
    
    db.commit()
    db.refresh(db_folder)
    return db_folder


def delete_folder(db: Session, folder_id: int) -> Optional[Folder]:
    db_folder = get_folder(db, folder_id)
    if not db_folder:
        return None
    
    db.delete(db_folder)
    db.commit()
    return db_folder


def get_folder_tree(db: Session, root_id: Optional[int] = None) -> List[folder_schemas.FolderWithChildren]:
    def build_tree(folders, parent_id):
        tree = []
        for folder in folders:
            if folder.parent_id == parent_id:
                folder_dict = folder_schemas.Folder.model_validate(folder).model_dump()
                children = build_tree(folders, folder.id)
                folder_with_children = folder_schemas.FolderWithChildren(
                    **folder_dict,
                    children=children
                )
                tree.append(folder_with_children)
        return tree
    
    all_folders = db.query(Folder).all()
    return build_tree(all_folders, root_id)
