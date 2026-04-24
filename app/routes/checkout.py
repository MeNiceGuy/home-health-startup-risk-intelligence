from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.services.payment import create_checkout_session
from app.routes.kits import KITS

router = APIRouter(prefix="/checkout", tags=["Checkout"])

@router.get("/{slug}")
def checkout_kit(slug: str):
    for kit_slug, title, price, desc, includes in KITS:
        if slug == kit_slug:
            url = create_checkout_session(title, price, slug)
            return RedirectResponse(url)

    return {"error": "Kit not found"}
