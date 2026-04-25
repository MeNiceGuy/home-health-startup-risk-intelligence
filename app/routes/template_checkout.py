import os
import stripe
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.services.settings import FREE_MODE, BASE_URL

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

router = APIRouter(prefix="/template-checkout", tags=["Template Checkout"])

PRODUCTS = {
    "revenue": {"name": "Revenue Cycle Starter Kit", "price": 19900},
    "operations": {"name": "Operations Workflow Kit", "price": 19900},
    "hiring": {"name": "Hiring & Retention Kit", "price": 17900},
    "compliance": {"name": "Compliance Policy Pack", "price": 19900}
}

@router.get("/{slug}")
def template_checkout(slug: str):
    product = PRODUCTS.get(slug)

    if not product:
        return {"error": "Template not found"}

    if FREE_MODE:
        return RedirectResponse(f"/templates/{slug}?session_id=free-demo-{slug}", status_code=303)

    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": product["name"]},
                "unit_amount": product["price"]
            },
            "quantity": 1
        }],
        success_url=f"{BASE_URL}/templates/{slug}?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{BASE_URL}/operating-audit/",
        metadata={
            "product_slug": slug,
            "product_type": "template",
            "amount": str(product["price"])
        }
    )

    return RedirectResponse(session.url)
