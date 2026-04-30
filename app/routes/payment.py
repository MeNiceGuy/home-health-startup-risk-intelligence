
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.services.payment import create_checkout_session

router = APIRouter(prefix="/pay")

@router.get("/")
def pay():
    url = create_checkout_session()
    return RedirectResponse(url)


