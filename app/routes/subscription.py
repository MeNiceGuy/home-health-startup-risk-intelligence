from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.services.subscription import create_subscription_checkout

router = APIRouter(prefix="/subscribe", tags=["Subscription"])

@router.get("/")
def subscribe():
    url = create_subscription_checkout()
    return RedirectResponse(url)
