import os
import stripe
from fastapi import APIRouter
from fastapi.responses import RedirectResponse, HTMLResponse
from app.services.settings import FREE_MODE, BASE_URL

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

router = APIRouter(prefix="/bundle", tags=["Bundle Checkout"])

BUNDLES = {
    "startup-stabilization": {
        "name": "Startup Operations Stabilization Bundle",
        "price": 79900,
        "desc": "Fix revenue cycle, operations, staffing, and compliance gaps together."
    },
    "targeted-growth": {
        "name": "Targeted Growth Repair Bundle",
        "price": 49900,
        "desc": "Fix the two highest-risk areas limiting client growth."
    }
}

@router.get("/{slug}")
def bundle_checkout(slug: str):
    bundle = BUNDLES.get(slug)

    if not bundle:
        return HTMLResponse("<h1>Bundle not found</h1>", status_code=404)

    if FREE_MODE:
        return HTMLResponse(f"""
        <html>
        <body style="font-family:Arial;background:#f8fafc;padding:40px;">
        <div style="max-width:800px;margin:auto;background:white;padding:35px;border-radius:18px;">
            <h1>{bundle["name"]}</h1>
            <p>{bundle["desc"]}</p>
            <h2>Demo Price: $0.00</h2>
            <p>FREE_MODE is active. In production, this will route to Stripe checkout.</p>
            <a href="/consultant/dashboard?tenant=demo"
            style="background:#16a34a;color:white;padding:14px 20px;border-radius:10px;text-decoration:none;">
            Continue
            </a>
        </div>
        </body>
        </html>
        """)

    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": bundle["name"]},
                "unit_amount": bundle["price"]
            },
            "quantity": 1
        }],
        success_url=f"{BASE_URL}/client/dashboard?email={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{BASE_URL}/operating-audit/",
        metadata={
            "product_slug": slug,
            "product_type": "bundle",
            "amount": str(bundle["price"])
        }
    )

    return RedirectResponse(session.url)


