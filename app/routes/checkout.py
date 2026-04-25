from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.services.payment import create_checkout_session
from app.routes.kits import KITS
from app.services.settings import FREE_MODE, BASE_URL

router = APIRouter(prefix="/checkout", tags=["Checkout"])

@router.get("/{slug}")
def checkout_kit(slug: str):
    if FREE_MODE:
        return RedirectResponse(f"/kits/{slug}", status_code=303)

    for kit_slug, title, price, desc, includes in KITS:
        if slug == kit_slug:
            url = create_checkout_session(title, price, slug)
            return RedirectResponse(url)

    if slug == "startup-compliance":
        url = create_checkout_session("Startup Compliance Fix Kit", 199, slug)
        return RedirectResponse(url)

    return {"error": "Kit not found"}
