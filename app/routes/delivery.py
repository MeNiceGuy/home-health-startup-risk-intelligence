from fastapi import APIRouter, Query
from fastapi.responses import FileResponse, HTMLResponse
from app.services.delivery import KIT_FILES
from app.services.tracking import init_db, save_purchase
import stripe
import os

router = APIRouter()

@router.get("/deliver/{slug}")
def deliver(slug: str, session_id: str = Query(None)):
    init_db()

    file_path = KIT_FILES.get(slug)

    if not file_path or not os.path.exists(file_path):
        return HTMLResponse("<h1>File not ready yet</h1>")

    customer_email = "unknown"

    if session_id:
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            customer_email = session.get("customer_details", {}).get("email", "unknown")
        except Exception:
            customer_email = "unknown"

        save_purchase(customer_email, slug, session_id)

    return FileResponse(file_path, filename=os.path.basename(file_path))
