from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from datetime import datetime
import csv, os

router = APIRouter()

EVENTS_FILE = "data/conversion_events.csv"

def track_event(event, source="unknown"):
    os.makedirs("data", exist_ok=True)
    exists = os.path.exists(EVENTS_FILE)

    with open(EVENTS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(["created_at", "event", "source"])
        writer.writerow([datetime.now().isoformat(timespec="seconds"), event, source])

@router.get("/track")
def track(event: str, source: str = "unknown", redirect: str = "/"):
    track_event(event, source)
    return RedirectResponse(redirect)

@router.get("/admin/conversions", response_class=HTMLResponse)
def conversion_dashboard():
    if not os.path.exists(EVENTS_FILE):
        return "<h1>No conversion events yet.</h1>"

    with open(EVENTS_FILE, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    total_views = len([r for r in rows if r["event"] == "upsell_view"])
    checkout_clicks = len([r for r in rows if r["event"] == "consulting_checkout_click"])
    booking_clicks = len([r for r in rows if r["event"] == "book_call_click"])

    checkout_rate = round((checkout_clicks / total_views) * 100, 1) if total_views else 0
    booking_rate = round((booking_clicks / total_views) * 100, 1) if total_views else 0

    html = f"""
    <html>
    <body style='font-family:Arial;background:#f8fafc;padding:40px;'>
        <h1>Conversion Dashboard</h1>

        <div style='display:grid;grid-template-columns:repeat(4,1fr);gap:15px;margin-bottom:25px;'>
            <div style='background:white;padding:20px;border-radius:14px;'><h3>Upsell Views</h3><h1>{total_views}</h1></div>
            <div style='background:white;padding:20px;border-radius:14px;'><h3>Checkout Clicks</h3><h1>{checkout_clicks}</h1></div>
            <div style='background:white;padding:20px;border-radius:14px;'><h3>Checkout Rate</h3><h1>{checkout_rate}%</h1></div>
            <div style='background:white;padding:20px;border-radius:14px;'><h3>Booking Rate</h3><h1>{booking_rate}%</h1></div>
        </div>

        <table border='1' cellpadding='10' style='background:white;border-collapse:collapse;width:100%;'>
            <tr><th>Date</th><th>Event</th><th>Source</th></tr>
    """

    for r in rows:
        html += f"<tr><td>{r['created_at']}</td><td>{r['event']}</td><td>{r['source']}</td></tr>"

    html += "</table></body></html>"
    return html


