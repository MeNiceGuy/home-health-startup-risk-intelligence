from fastapi import APIRouter
from fastapi.responses import RedirectResponse
import os
import stripe
from app.kit_catalog import KIT_PRICES

router = APIRouter()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")

@router.get("/kit-checkout/{slug}")
def kit_checkout(slug: str):
    kit = KIT_PRICES.get(slug)

    if not kit:
        return RedirectResponse("/")

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": kit["name"]},
                "unit_amount": kit["amount"],
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=f"http://127.0.0.1:8000/templates/{slug}?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"http://127.0.0.1:8000/kits",
    )

    return RedirectResponse(session.url)


