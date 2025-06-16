from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.config import settings
from src.telegram.auth_service import AuthService

router = APIRouter(prefix="", tags=["Auth Bots"])
auth_service = AuthService(session_dir=settings.SESSIONS_DIR)

class AuthRequest(BaseModel):
    phone: str
    api_id: int
    api_hash: str

class CodeSubmit(BaseModel):
    code: str
    phone: str
    api_id: int
    api_hash: str

class PasswordSubmit(BaseModel):
    password: str
    phone: str
    api_id: int
    api_hash: str

@router.post("/auth/request_code/")
async def request_code(data: AuthRequest):
    try:
        await auth_service.request_code(data.phone, data.api_id, data.api_hash)
        return {"status": "code sent"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/auth/submit_code/")
async def submit_code(data: CodeSubmit):
    result = await auth_service.submit_code(data.phone, data.code, data.api_id, data.api_hash)
    return {"status": result}

@router.post("/auth/submit_password/")
async def submit_code(data: PasswordSubmit):
    result = await auth_service.submit_password(data.phone, data.password, data.api_id, data.api_hash)
    return {"status": result}