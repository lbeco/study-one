# study-one 后端技术架构

## 技术栈选型

### Web 框架
- **FastAPI** - 现代、快速（高性能）的 Web 框架，用于基于标准 Python 类型提示使用 Python 3.7+ 构建 API
  - 异步支持
  - 自动生成 API 文档（Swagger/OpenAPI）
  - 类型提示支持
  - 性能优秀

### 数据库
- **SQLite** - 轻量级关系型数据库
- **SQLAlchemy 2.0** - ORM 框架，支持异步
- **Alembic** - 数据库迁移工具

### 其他核心依赖
- **Pydantic** - 数据验证和设置管理（FastAPI 自带）
- **python-dotenv** - 环境变量管理
- **beautifulsoup4** - 网页解析
- **requests** - HTTP 请求（用于网页抓取）
- **markdown** - Markdown 解析
- **python-multipart** - 文件上传支持

---

## 数据库设计

### 核心表结构

#### 1. folders（文件夹表）
```sql
CREATE TABLE folders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    parent_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES folders(id) ON DELETE CASCADE
);
```

#### 2. knowledge_items（知识项表）
```sql
CREATE TABLE knowledge_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,  -- 'markdown' | 'webpage'
    content TEXT,
    folder_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (folder_id) REFERENCES folders(id) ON DELETE SET NULL
);
```

#### 3. markdown_contents（Markdown 内容表）
```sql
CREATE TABLE markdown_contents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    knowledge_item_id INTEGER NOT NULL,
    file_path VARCHAR(500) NOT NULL,  -- 文件系统中的路径
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (knowledge_item_id) REFERENCES knowledge_items(id) ON DELETE CASCADE
);
```

#### 4. webpage_contents（网页内容表）
```sql
CREATE TABLE webpage_contents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    knowledge_item_id INTEGER NOT NULL,
    url VARCHAR(1000) NOT NULL,
    title VARCHAR(255),
    description TEXT,
    summary TEXT,
    keywords TEXT,
    fetched_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (knowledge_item_id) REFERENCES knowledge_items(id) ON DELETE CASCADE
);
```

#### 5. tags（标签表）
```sql
CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    color VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 6. knowledge_tags（知识-标签关联表）
```sql
CREATE TABLE knowledge_tags (
    knowledge_item_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (knowledge_item_id, tag_id),
    FOREIGN KEY (knowledge_item_id) REFERENCES knowledge_items(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);
```

#### 7. learning_records（学习记录表）
```sql
CREATE TABLE learning_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    knowledge_item_id INTEGER NOT NULL,
    question TEXT NOT NULL,
    answer TEXT,
    is_correct BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (knowledge_item_id) REFERENCES knowledge_items(id) ON DELETE CASCADE
);
```

---

## 文件系统存储结构

### 数据目录布局
```
study-one/
├── data/
│   ├── study_one.db          # SQLite 数据库文件
│   └── knowledge/
│       ├── markdown/
│       │   ├── {uuid1}.md
│       │   ├── {uuid2}.md
│       │   └── ...
│       └── attachments/      # 附件（图片等）
│           ├── {uuid1}.png
│           └── ...
└── ...
```

### 文件命名规则
- 使用 UUID 作为文件名，避免冲突
- Markdown 文件：`{uuid}.md`
- 附件文件：保留原始扩展名

---

## API 接口设计

### RESTful API 规范
- 使用 `/api/v1` 作为 API 前缀
- 使用 HTTP 动词：GET, POST, PUT, DELETE
- 统一响应格式

### 统一响应格式
```json
{
  "success": true,
  "data": {},
  "message": "操作成功"
}
```

### 文件夹管理 API

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/v1/folders` | 获取所有文件夹 |
| GET | `/api/v1/folders/{id}` | 获取单个文件夹 |
| POST | `/api/v1/folders` | 创建文件夹 |
| PUT | `/api/v1/folders/{id}` | 更新文件夹 |
| DELETE | `/api/v1/folders/{id}` | 删除文件夹 |
| GET | `/api/v1/folders/{id}/tree` | 获取文件夹树 |

### 知识项管理 API

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/v1/knowledge` | 获取知识列表（支持分页、搜索、筛选） |
| GET | `/api/v1/knowledge/{id}` | 获取单个知识项 |
| POST | `/api/v1/knowledge` | 创建知识项 |
| PUT | `/api/v1/knowledge/{id}` | 更新知识项 |
| DELETE | `/api/v1/knowledge/{id}` | 删除知识项 |
| GET | `/api/v1/knowledge/search?q=xxx` | 搜索知识 |

### Markdown 内容 API

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/v1/knowledge/{id}/markdown` | 获取 Markdown 文件内容（从文件系统读取） |
| PUT | `/api/v1/knowledge/{id}/markdown` | 更新 Markdown 文件内容（写入文件系统） |
| POST | `/api/v1/knowledge/markdown/upload` | 上传 Markdown 文件 |

### 网页内容 API

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/v1/knowledge/{id}/webpage` | 获取网页内容 |
| POST | `/api/v1/knowledge/{id}/webpage` | 创建/更新网页内容 |
| POST | `/api/v1/knowledge/webpage/fetch` | 抓取网页信息 |

### 标签管理 API

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/v1/tags` | 获取所有标签 |
| POST | `/api/v1/tags` | 创建标签 |
| PUT | `/api/v1/tags/{id}` | 更新标签 |
| DELETE | `/api/v1/tags/{id}` | 删除标签 |
| POST | `/api/v1/knowledge/{id}/tags` | 给知识项添加标签 |
| DELETE | `/api/v1/knowledge/{id}/tags/{tag_id}` | 移除知识项的标签 |

---

## 项目目录结构

```
study-one/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI 应用入口
│   │   ├── config.py            # 配置管理
│   │   ├── database.py          # 数据库连接
│   │   │
│   │   ├── models/              # 数据库模型
│   │   │   ├── __init__.py
│   │   │   ├── folder.py
│   │   │   ├── knowledge.py
│   │   │   ├── markdown.py
│   │   │   ├── webpage.py
│   │   │   ├── tag.py
│   │   │   └── learning.py
│   │   │
│   │   ├── schemas/             # Pydantic 模式
│   │   │   ├── __init__.py
│   │   │   ├── folder.py
│   │   │   ├── knowledge.py
│   │   │   ├── markdown.py
│   │   │   ├── webpage.py
│   │   │   ├── tag.py
│   │   │   └── common.py
│   │   │
│   │   ├── crud/                # 数据库操作
│   │   │   ├── __init__.py
│   │   │   ├── folder.py
│   │   │   ├── knowledge.py
│   │   │   ├── markdown.py
│   │   │   ├── webpage.py
│   │   │   └── tag.py
│   │   │
│   │   ├── api/                 # API 路由
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── folders.py
│   │   │   │   ├── knowledge.py
│   │   │   │   ├── markdown.py
│   │   │   │   ├── webpage.py
│   │   │   │   └── tags.py
│   │   │
│   │   ├── services/            # 业务逻辑
│   │   │   ├── __init__.py
│   │   │   ├── webpage_fetcher.py
│   │   │   └── search_service.py
│   │   │
│   │   └── utils/               # 工具函数
│   │       ├── __init__.py
│   │       └── helpers.py
│   │
│   ├── alembic/                 # 数据库迁移
│   │   ├── versions/
│   │   └── env.py
│   │
│   ├── tests/                   # 测试
│   │   ├── __init__.py
│   │   └── test_api.py
│   │
│   ├── .env.example             # 环境变量示例
│   ├── requirements.txt         # Python 依赖
│   └── alembic.ini
│
└── frontend/                    # Vue 前端（后续实现）
```

---

## 核心模块设计

### 1. 网页抓取服务 (webpage_fetcher.py)
```python
class WebpageFetcher:
    async def fetch(self, url: str) -> dict:
        """
        抓取网页信息
        返回: title, description, summary, keywords
        """
        pass

    def extract_content(self, html: str) -> dict:
        """
        从 HTML 中提取关键信息
        """
        pass
```

### 2. 搜索服务 (search_service.py)
```python
class SearchService:
    async def search(self, query: str) -> list:
        """
        搜索知识项
        """
        pass

    async def search_by_tags(self, tags: list) -> list:
        """
        按标签搜索
        """
        pass
```

### 3. 文件服务 (file_service.py)
```python
class FileService:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self._ensure_dirs()

    def _ensure_dirs(self):
        """确保必要的目录存在"""
        pass

    async def save_markdown(self, content: str, filename: str = None) -> str:
        """
        保存 Markdown 内容到文件系统
        返回文件路径
        """
        pass

    async def read_markdown(self, file_path: str) -> str:
        """
        从文件系统读取 Markdown 内容
        """
        pass

    async def update_markdown(self, file_path: str, content: str):
        """
        更新 Markdown 文件内容
        """
        pass

    async def delete_file(self, file_path: str):
        """
        删除文件
        """
        pass

    def get_full_path(self, relative_path: str) -> str:
        """
        获取文件的完整路径
        """
        pass
```

---

## 配置说明

### 环境变量 (.env)
```env
# 数据库
DATABASE_URL=sqlite:///./data/study_one.db

# 应用
APP_NAME=study-one
DEBUG=true

# 文件存储
UPLOAD_DIR=./uploads
```

---

## 下一步
1. 初始化后端项目
2. 创建数据库模型
3. 实现基础 API
4. 实现网页抓取功能
