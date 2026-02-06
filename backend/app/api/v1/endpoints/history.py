from fastapi import APIRouter

router = APIRouter()


@router.get("/list")
async def list_history():
    """获取评测历史列表"""
    return {"message": "History list endpoint"}


@router.get("/progress/{user_id}")
async def get_progress(user_id: str):
    """获取进步曲线"""
    return {"user_id": user_id}


@router.get("/statistics/{user_id}")
async def get_statistics(user_id: str):
    """获取统计数据"""
    return {"user_id": user_id}
