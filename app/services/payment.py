import os
import stripe

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def create_checkout_session(name, amount):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": name},
                "unit_amount": int(amount * 100),
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url="https://home-health-startup-risk-intelligence.onrender.com/success",
        cancel_url="https://home-health-startup-risk-intelligence.onrender.com/kits/",
    )
    return session.url
