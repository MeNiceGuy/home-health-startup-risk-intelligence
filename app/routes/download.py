from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/download-kit")
def download_kit(file: str):
    return FileResponse(file, filename=file.split("\\")[-1])
