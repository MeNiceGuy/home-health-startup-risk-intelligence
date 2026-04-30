import csv, os
from datetime import datetime
from app.kit_catalog import KIT_PRICES
from app.services.smtp_sender import send_email

ORDERS_FILE = "data/orders.csv"

def save_order(email, cart):
    os.makedirs("data", exist_ok=True)
    exists = os.path.exists(ORDERS_FILE)

    total = sum(KIT_PRICES.get(slug, {}).get("amount", 0) for slug in cart)

    with open(ORDERS_FILE, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(["created_at","email","items","total_cents","status"])
        w.writerow([datetime.now().isoformat(timespec="seconds"), email, ",".join(cart), total, "paid"])

    return total

def build_delivery_html(cart):
    html = "<ul>"
    for slug in cart:
        kit = KIT_PRICES.get(slug)
        if kit:
            html += f"<li><strong>{kit['name']}</strong> — <a href='/template/{slug}'>Open Kit</a></li>"
    html += "</ul>"
    return html

def send_purchase_receipt(email, cart):
    if not email:
        return False

    items = "\n".join([KIT_PRICES.get(slug, {}).get("name", slug) for slug in cart])
    body = f"""
Thank you for your purchase.

Your implementation systems are ready:

{items}

Access your dashboard:
http://127.0.0.1:8000/kits

Best,
Home Health Performance Intelligence
"""
    return send_email(email, "Your Implementation Systems Are Ready", body)


