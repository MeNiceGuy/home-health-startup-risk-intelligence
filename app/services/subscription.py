import os
import stripe

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def create_subscription_checkout():
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="subscription",
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": "Operating Intelligence Subscription"},
                "unit_amount": 9900,
                "recurring": {"interval": "month"}
            },
            "quantity": 1
        }],
        success_url="https://home-health-startup-risk-intelligence.onrender.com/subscribe/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="https://home-health-startup-risk-intelligence.onrender.com/operating-audit/"
    )
    return session.url
