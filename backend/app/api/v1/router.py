from fastapi import APIRouter
from app.api.v1.endpoints import essays, history, examples, models, users

api_router = APIRouter()

api_router.include_router(
    essays.router,
    prefix="/essays",
    tags=["作文评测"]
)

api_router.include_router(
    history.router,
    prefix="/history",
    tags=["历史记录"]
)

api_router.include_router(
    examples.router,
    prefix="/examples",
    tags=["范文库"]
)

api_router.include_router(
    models.router,
    prefix="/models",
    tags=["模型配置"]
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["用户管理"]
)
