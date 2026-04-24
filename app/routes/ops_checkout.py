from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.services.payment import create_checkout_session
from app.services.operating_kits import OPERATING_KITS

router = APIRouter(prefix="/ops-checkout", tags=["Operating Checkout"])

@router.get("/{slug}")
def checkout(slug: str):
    kit = OPERATING_KITS.get(slug)
    if not kit:
        return {"error": "Invalid product"}

    url = create_checkout_session(kit["name"], kit["price"], slug)
    return RedirectResponse(url)
