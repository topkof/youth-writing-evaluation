from fastapi import APIRouter

router = APIRouter()


@router.get("/list")
async def list_examples():
    """获取范文列表"""
    return {"message": "Examples list endpoint"}


@router.get("/{example_id}")
async def get_example(example_id: str):
    """获取范文详情"""
    return {"example_id": example_id}
