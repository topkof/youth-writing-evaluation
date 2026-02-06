from fastapi import APIRouter

router = APIRouter()


@router.get("/list")
async def list_models():
    """获取模型配置列表"""
    return {"message": "Models list endpoint"}


@router.post("/test")
async def test_model():
    """测试模型连接"""
    return {"message": "Test model endpoint"}


@router.post("/add")
async def add_model():
    """添加模型配置"""
    return {"message": "Add model endpoint"}
