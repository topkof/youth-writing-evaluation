from fastapi import APIRouter

router = APIRouter()


@router.post("/register")
async def register():
    """用户注册"""
    return {"message": "Register endpoint"}


@router.post("/login")
async def login():
    """用户登录"""
    return {"message": "Login endpoint"}


@router.get("/profile")
async def get_profile():
    """获取用户资料"""
    return {"message": "Profile endpoint"}
