import os
import stripe

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def create_checkout_session(product_name, amount, slug):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": product_name},
                "unit_amount": int(amount * 100),
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=f"https://home-health-startup-risk-intelligence.onrender.com/deliver/{slug}?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url="https://home-health-startup-risk-intelligence.onrender.com/kits/",
    )
    return session.url
