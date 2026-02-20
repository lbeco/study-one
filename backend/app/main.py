from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRouter

from .config import settings
from .database import engine, Base
from .models import (
    Folder,
    KnowledgeItem,
    MarkdownContent,
    WebpageContent,
    Tag,
    LearningRecord
)
from .api.v1 import folders, tags, knowledge, markdown, webpage

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# API v1 路由
api_v1_router = APIRouter(prefix="/api/v1")

# 注册所有路由
api_v1_router.include_router(folders.router)
api_v1_router.include_router(tags.router)
api_v1_router.include_router(knowledge.router)
api_v1_router.include_router(markdown.router)
api_v1_router.include_router(webpage.router)

# 将 API 路由注册到主应用
app.include_router(api_v1_router)


@app.get("/")
async def root():
    return {"message": "Welcome to study-one!", "app": settings.APP_NAME}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
