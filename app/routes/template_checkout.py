from fastapi import APIRouter
from fastapi.responses import RedirectResponse
import os
import stripe

router = APIRouter()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")

TEMPLATE_PRICES = {
    "operations": 12900,
    "compliance": 19900,
    "hiring": 14900,
    "revenue": 19900
}

@router.get("/template-checkout/{slug}")
def template_checkout(slug: str):
    amount = TEMPLATE_PRICES.get(slug, 12900)

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": f"{slug.title()} Template Pack"},
                "unit_amount": amount,
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=f"http://127.0.0.1:8000/templates/{slug}?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"http://127.0.0.1:8000/template-cancel/{slug}",
    )

    return RedirectResponse(session.url)

@router.get("/template-cancel/{slug}")
def template_cancel(slug: str):
    return RedirectResponse(f"/template-checkout/{slug}")


