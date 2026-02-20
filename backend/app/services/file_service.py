import os
import uuid
from pathlib import Path
from typing import Optional

from ..config import settings


class FileService:
    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = Path(base_dir or settings.DATA_DIR)
        self.markdown_dir = self.base_dir / "knowledge" / "markdown"
        self.attachments_dir = self.base_dir / "knowledge" / "attachments"
        self._ensure_dirs()

    def _ensure_dirs(self):
        self.markdown_dir.mkdir(parents=True, exist_ok=True)
        self.attachments_dir.mkdir(parents=True, exist_ok=True)

    def save_markdown(self, content: str, filename: Optional[str] = None) -> str:
        if not filename:
            filename = f"{uuid.uuid4()}.md"
        file_path = self.markdown_dir / filename
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return str(file_path.relative_to(self.base_dir))

    def read_markdown(self, relative_path: str) -> str:
        full_path = self.get_full_path(relative_path)
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()

    def update_markdown(self, relative_path: str, content: str):
        full_path = self.get_full_path(relative_path)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

    def delete_file(self, relative_path: str):
        full_path = self.get_full_path(relative_path)
        if full_path.exists():
            full_path.unlink()

    def get_full_path(self, relative_path: str) -> Path:
        return self.base_dir / relative_path


file_service = FileService()
