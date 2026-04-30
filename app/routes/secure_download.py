from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
from app.routes.auth import get_current_user
import os

router = APIRouter()

@router.get("/download/{file_id}")
def secure_download(file_id: str, request: Request):
    user = get_current_user(request)
    if not user:
        return {"error":"unauthorized"}

    path = f"generated_kits/{file_id}.pdf"
    if not os.path.exists(path):
        return {"error":"not found"}

    return FileResponse(path)


