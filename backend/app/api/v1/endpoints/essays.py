from fastapi import APIRouter

router = APIRouter()


@router.post("/evaluate")
async def evaluate_essay():
    """评测单篇作文"""
    return {"message": "Essay evaluation endpoint"}


@router.post("/batch-evaluate")
async def batch_evaluate():
    """批量评测作文"""
    return {"message": "Batch evaluation endpoint"}


@router.get("/result/{essay_id}")
async def get_evaluation_result(essay_id: str):
    """获取评测结果"""
    return {"essay_id": essay_id}
