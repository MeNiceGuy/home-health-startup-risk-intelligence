from fastapi import APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from app.kit_catalog import KIT_PRICES
import os
import stripe

router = APIRouter()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")

CART = []

def cart_totals():
    subtotal = sum(KIT_PRICES[slug]["amount"] for slug in CART if slug in KIT_PRICES)

    discount_rate = 0
    if len(CART) >= 3:
        discount_rate = 0.25
    elif len(CART) >= 2:
        discount_rate = 0.15

    discount = int(subtotal * discount_rate)
    total = subtotal - discount

    return subtotal, discount, total, discount_rate

@router.get("/cart/add/{slug}")
def add_to_cart(slug: str):
    if slug in KIT_PRICES and slug not in CART:
        CART.append(slug)
    return RedirectResponse("/cart")

@router.get("/cart/remove/{slug}")
def remove_from_cart(slug: str):
    if slug in CART:
        CART.remove(slug)
    return RedirectResponse("/cart")

@router.get("/cart/clear")
def clear_cart():
    CART.clear()
    return RedirectResponse("/cart")

@router.get("/cart", response_class=HTMLResponse)
def view_cart():
    subtotal, discount, total, discount_rate = cart_totals()

    items_html = ""
    for slug in CART:
        kit = KIT_PRICES[slug]
        price = kit["amount"] / 100
        items_html += f"""
        <div style='display:flex;justify-content:space-between;align-items:center;background:white;padding:16px;border-radius:12px;margin-bottom:10px;border:1px solid #e5e7eb;'>
            <div>
                <strong>{kit["name"]}</strong><br>
                <span>${price:,.0f}</span>
            </div>
            <a href='/cart/remove/{slug}' style='color:#dc2626;font-weight:bold;text-decoration:none;'>Remove</a>
        </div>
        """

    if not CART:
        items_html = "<p>Your cart is empty.</p>"

    checkout_button = ""
    if CART:
        checkout_button = """
        <a href="/bundle-checkout"
           style="display:block;background:#dc2626;color:white;text-align:center;padding:16px;border-radius:12px;text-decoration:none;font-weight:bold;font-size:18px;margin-top:20px;">
           Checkout Bundle with Stripe
        </a>
        """

    return f"""
    <html>
    <body style='font-family:Arial;background:#f8fafc;padding:40px;'>
        <div style='max-width:820px;margin:auto;background:#ffffff;padding:35px;border-radius:20px;box-shadow:0 10px 30px rgba(0,0,0,.08);'>
            <h1>Your Implementation Bundle</h1>
            <p>Bundle kits together to increase execution power and reduce total cost.</p>

            {items_html}

            <hr>

            <p>Subtotal: <strong>${subtotal/100:,.0f}</strong></p>
            <p>Bundle Discount: <strong style='color:#16a34a;'>-${discount/100:,.0f}</strong> ({int(discount_rate*100)}%)</p>
            <h2>Total: ${total/100:,.0f}</h2>

            {checkout_button}

            <br>
            <a href='/kits'>Continue Shopping</a> |
            <a href='/cart/clear'>Clear Cart</a>
        </div>
    </body>
    </html>
    """

@router.get("/bundle-checkout")
def bundle_checkout():
    subtotal, discount, total, discount_rate = cart_totals()

    if not CART or total <= 0:
        return RedirectResponse("/kits")

    names = ", ".join(KIT_PRICES[slug]["name"] for slug in CART if slug in KIT_PRICES)

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": f"Implementation Bundle: {names}",
                    "description": f"Bundle discount applied: {int(discount_rate*100)}%"
                },
                "unit_amount": total,
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url="http://127.0.0.1:8000/bundle-success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="http://127.0.0.1:8000/cart",
    )

    return RedirectResponse(session.url)

@router.get("/bundle-success", response_class=HTMLResponse)
def bundle_success(session_id: str = ""):
    purchased = list(CART)
    CART.clear()

    links = ""
    for slug in purchased:
        links += f"<li><a href='/templates/{slug}?session_id={session_id}'>{KIT_PRICES[slug]['name']}</a></li>"

    return f"""
    <html>
    <body style='font-family:Arial;background:#f8fafc;padding:40px;'>
        <div style='max-width:760px;margin:auto;background:white;padding:35px;border-radius:18px;box-shadow:0 8px 24px rgba(0,0,0,.08);'>
            <h1 style='color:#16a34a;'>Bundle Purchase Successful</h1>
            <p>Your implementation kits are ready.</p>
            <ul>{links}</ul>
            <a href='/upsell/consulting'>Upgrade to Full Implementation</a>
        </div>
    </body>
    </html>
    """

@router.get("/cart/add-bundle")
def add_bundle(kits: str = ""):
    selected = [x.strip() for x in kits.split(",") if x.strip()]

    # Full Optimization includes all individual kits.
    # If selected, remove smaller kits and only keep full system.
    if "full-optimization" in selected:
        CART.clear()
        CART.append("full-optimization")
        return RedirectResponse("/cart")

    for slug in selected:
        if slug in KIT_PRICES and slug not in CART:
            CART.append(slug)

    return RedirectResponse("/cart")


