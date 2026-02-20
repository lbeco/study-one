# 数据库操作层 (CRUD) 实现计划

## 现有数据库模型分析

### 核心模型
1. **Folder** - 文件夹
2. **KnowledgeItem** - 知识项
3. **MarkdownContent** - Markdown 内容
4. **WebpageContent** - 网页内容
5. **Tag** - 标签
6. **LearningRecord** - 学习记录

### 关联关系
- Folder → KnowledgeItem (一对多)
- KnowledgeItem → MarkdownContent (一对一)
- KnowledgeItem → WebpageContent (一对一)
- KnowledgeItem ↔ Tag (多对多)
- KnowledgeItem → LearningRecord (一对多)

## CRUD 操作设计

### 1. 基础 CRUD 操作

#### Folder CRUD
- **Create**: 创建文件夹
- **Read**: 获取单个文件夹、获取文件夹列表、获取文件夹树结构
- **Update**: 更新文件夹信息
- **Delete**: 删除文件夹

#### KnowledgeItem CRUD
- **Create**: 创建知识项
- **Read**: 获取单个知识项详情、获取知识项列表（支持分页、搜索、筛选）
- **Update**: 更新知识项信息
- **Delete**: 删除知识项

#### MarkdownContent CRUD
- **Create**: 创建 Markdown 内容（包括文件存储）
- **Read**: 读取 Markdown 内容（包括文件读取）
- **Update**: 更新 Markdown 内容（包括文件更新）
- **Delete**: 删除 Markdown 内容（包括文件删除）

#### WebpageContent CRUD
- **Create**: 创建网页内容
- **Read**: 读取网页内容
- **Update**: 更新网页内容
- **Delete**: 删除网页内容

#### Tag CRUD
- **Create**: 创建标签
- **Read**: 获取标签列表
- **Update**: 更新标签
- **Delete**: 删除标签

#### LearningRecord CRUD
- **Create**: 创建学习记录
- **Read**: 获取学习记录列表
- **Delete**: 删除学习记录

### 2. 关联操作

#### KnowledgeItem 与 Tag 关联
- **Add Tag**: 为知识项添加标签
- **Remove Tag**: 从知识项移除标签
- **Get By Tags**: 按标签查询知识项

#### KnowledgeItem 与 MarkdownContent 关联
- **Create With Markdown**: 创建知识项并关联 Markdown 内容

#### KnowledgeItem 与 WebpageContent 关联
- **Create With Webpage**: 创建知识项并关联网页内容
- **Fetch Webpage**: 抓取网页并创建/更新内容

## 实现计划

### 第一阶段：基础 CRUD 实现
1. **Create crud/__init__.py** - 导出所有 CRUD 操作
2. **Implement folder.py** - 文件夹 CRUD
3. **Implement tag.py** - 标签 CRUD
4. **Implement knowledge.py** - 知识项 CRUD
5. **Implement markdown.py** - Markdown 内容 CRUD
6. **Implement webpage.py** - 网页内容 CRUD
7. **Implement learning.py** - 学习记录 CRUD

### 第二阶段：关联操作实现
1. **Enhance knowledge.py** - 添加标签关联操作
2. **Enhance knowledge.py** - 添加 Markdown/Webpage 关联操作
3. **Implement search functionality** - 搜索功能

### 第三阶段：测试与优化
1. **Add error handling** - 错误处理
2. **Add transaction support** - 事务支持
3. **Add performance optimizations** - 性能优化

## 技术实现要点

### 1. 目录结构
```python
app/crud/
├── __init__.py        # 导出所有 CRUD 操作
├── folder.py          # 文件夹 CRUD
├── knowledge.py       # 知识项 CRUD
├── markdown.py        # Markdown 内容 CRUD
├── webpage.py         # 网页内容 CRUD
├── tag.py             # 标签 CRUD
└── learning.py        # 学习记录 CRUD
```

### 2. 实现模式
每个 CRUD 模块采用以下模式：

```python
from sqlalchemy.orm import Session
from typing import Optional, List

from ..models import ModelName
from ..schemas import ModelNameCreate, ModelNameUpdate


def get_item(db: Session, item_id: int) -> Optional[ModelName]:
    pass

def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[ModelName]:
    pass

def create_item(db: Session, item: ModelNameCreate) -> ModelName:
    pass

def update_item(db: Session, item_id: int, item: ModelNameUpdate) -> Optional[ModelName]:
    pass

def delete_item(db: Session, item_id: int) -> Optional[ModelName]:
    pass
```

### 3. 特殊操作

#### 文件夹树结构
```python
def get_folder_tree(db: Session, root_id: Optional[int] = None) -> List[FolderWithChildren]:
    """获取文件夹树结构"""
    pass
```

#### 知识项搜索
```python
def search_knowledge(db: Session, query: str, skip: int = 0, limit: int = 100) -> List[KnowledgeItem]:
    """搜索知识项"""
    pass
```

#### 按标签查询
```python
def get_knowledge_by_tags(db: Session, tag_ids: List[int], skip: int = 0, limit: int = 100) -> List[KnowledgeItem]:
    """按标签查询知识项"""
    pass
```

## 已澄清的问题

### 1. 分页实现
- **分页参数**: `page` + `page_size`
- **默认值**: 每页默认显示 20 条记录

### 2. 搜索功能
- **搜索范围**: 全部字段（标题、内容、标签等）
- **搜索算法**: 使用简单的 LIKE 查询

### 3. 事务处理
- **关联操作**: 创建知识项并关联内容时，使用事务
- **错误处理**: 遇到错误时自动回滚操作

### 4. 性能考虑
- **批量操作**: 暂时不支持，后续可根据需求添加
- **缓存**: 暂时不使用缓存，后续可根据性能需求添加

### 5. 特殊场景
- **文件夹删除**: 删除文件夹时，一并删除其中的所有知识项（级联删除）
- **标签删除**: 删除标签时，自动解除与知识项的关联

## 预期输出

完成后，API 层将能够通过调用 CRUD 操作来实现：
- 完整的文件夹管理功能
- 知识项的增删改查
- Markdown 文件的上传和管理
- 网页内容的抓取和管理
- 标签的管理和使用
- 学习记录的管理

通过这个 CRUD 层，我们将为前端提供完整的数据操作能力。