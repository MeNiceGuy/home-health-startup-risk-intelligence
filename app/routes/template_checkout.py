import os
import stripe
from fastapi import APIRouter
from fastapi.responses import RedirectResponse

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

router = APIRouter(prefix="/template-checkout", tags=["Template Checkout"])

PRODUCTS = {
    "revenue": {
        "name": "Revenue Cycle Starter Kit",
        "price": 19900
    },
    "operations": {
        "name": "Operations Workflow Kit",
        "price": 19900
    },
    "hiring": {
        "name": "Hiring & Retention Kit",
        "price": 17900
    },
    "compliance": {
        "name": "Compliance Policy Pack",
        "price": 19900
    }
}

@router.get("/{slug}")
def template_checkout(slug: str):
    product = PRODUCTS.get(slug)

    if not product:
        return {"error": "Template not found"}

    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": product["name"]
                },
                "unit_amount": product["price"]
            },
            "quantity": 1
        }],
        success_url=f"https://home-health-startup-risk-intelligence.onrender.com/templates/{slug}?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url="https://home-health-startup-risk-intelligence.onrender.com/operating-audit/"
    )

    return RedirectResponse(session.url)
