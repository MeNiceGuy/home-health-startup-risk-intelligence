import os
import stripe

from app.kit_catalog import KIT_PRICES



stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


def create_bundle_checkout(cart):
    base_url = os.getenv("BASE_URL", "http://127.0.0.1:8000")

    line_items = []

    for slug in cart:
        kit = KIT_PRICES.get(slug)
        if not kit:
            continue

        line_items.append({
            "price_data": {
                "currency": "usd",
                "product_data": {"name": kit["name"]},
                "unit_amount": kit["amount"]
            },
            "quantity": 1
        })

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=f"{base_url}/payment-success",
        cancel_url=f"{base_url}/cart"
    )

    return session.url


def create_audit_checkout():
    import os
    base_url = os.getenv("BASE_URL", "http://127.0.0.1:8000")

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": "Full Performance Audit"},
                "unit_amount": 19900
            },
            "quantity": 1
        }],
        mode="payment",
        success_url=f"{base_url}/audit-unlock",
        cancel_url=f"{base_url}/pricing"
    )

    return session.url


def create_paid_audit_checkout():
    import os
    base_url = os.getenv("BASE_URL", "http://127.0.0.1:8000")

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": "Full Home Health Revenue Performance Audit",
                    "description": "Includes revenue risk estimate, opportunity score, roadmap, and executive PDF."
                },
                "unit_amount": 19900
            },
            "quantity": 1
        }],
        mode="payment",
        success_url=f"{base_url}/audit-success?paid=1",
        cancel_url=f"{base_url}/audit-checkout"
    )

    return session.url

