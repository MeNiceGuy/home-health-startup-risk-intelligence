from fastapi import APIRouter, Query
from fastapi.responses import RedirectResponse
from app.services.tenants import init_tenants, get_conn, USE_POSTGRES
import re

router = APIRouter(prefix="/onboard", tags=["Free Onboarding"])

def clean_subdomain(name):
    return re.sub(r"[^a-z0-9]", "", name.lower())[:20] or "demo"

@router.get("/create-free")
def create_free_tenant(
    name: str = Query("Demo Consultant"),
    email: str = Query("demo@example.com"),
    color: str = Query("#2563eb"),
    stripe_account: str = Query("")
):
    init_tenants()
    subdomain = clean_subdomain(name)

    conn = get_conn()
    cur = conn.cursor()

    if USE_POSTGRES:
        cur.execute("""
        INSERT INTO tenants (name, subdomain, primary_color, stripe_account)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (subdomain) DO NOTHING
        """, (name, subdomain, color, stripe_account))
    else:
        cur.execute("""
        INSERT OR IGNORE INTO tenants (name, subdomain, primary_color, stripe_account)
        VALUES (?, ?, ?, ?)
        """, (name, subdomain, color, stripe_account))

    conn.commit()
    conn.close()

    return RedirectResponse(f"/consultant/dashboard?tenant={subdomain}", status_code=303)
