import os
import stripe
from fastapi import APIRouter, Form
from fastapi.responses import RedirectResponse
from app.services.settings import FREE_MODE, BASE_URL

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

router = APIRouter(prefix="/consultant-subscribe", tags=["Consultant Subscription"])

@router.post("/checkout")
def consultant_subscription_checkout(
    name: str = Form(...),
    email: str = Form(...),
    color_select: str = Form(""),
    color_custom: str = Form(""),
    stripe_account: str = Form("")
):
    color = color_custom if color_custom else color_select

    if FREE_MODE:
        return RedirectResponse(
            f"/onboard/create-free?name={name}&email={email}&color={color}&stripe_account={stripe_account}",
            status_code=303
        )

    session = stripe.checkout.Session.create(
        mode="subscription",
        payment_method_types=["card"],
        customer_email=email,
        line_items=[{
            "price_data": {
                "currency": "usd",
                "recurring": {"interval": "month"},
                "product_data": {"name": "White-Label Consultant Platform"},
                "unit_amount": 19900
            },
            "quantity": 1
        }],
        metadata={
            "name": name,
            "email": email,
            "color": color,
            "stripe_account": stripe_account,
            "product_type": "consultant_subscription"
        },
        success_url=f"{BASE_URL}/onboard/success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{BASE_URL}/onboard/"
    )

    return RedirectResponse(session.url, status_code=303)


