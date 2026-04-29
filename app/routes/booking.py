from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from datetime import datetime
import csv, os

router = APIRouter()

BOOKINGS_FILE = "data/bookings.csv"

def save_booking(name, email, agency, phone, preferred_time, notes):
    os.makedirs("data", exist_ok=True)
    exists = os.path.exists(BOOKINGS_FILE)

    with open(BOOKINGS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not exists:
            writer.writerow(["created_at","name","email","agency","phone","preferred_time","notes","status","deal_value"])

        writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            name,email,agency,phone,preferred_time,notes,"new",2999
        ])

@router.get("/book-call", response_class=HTMLResponse)
def book_call_page():
    return """
    <html>
    <body style='font-family:Arial;background:#f8fafc;padding:40px;'>
        <div style='max-width:760px;margin:auto;background:white;padding:35px;border-radius:18px;box-shadow:0 8px 24px rgba(0,0,0,.08);'>
            <h1>Book Your Revenue Recovery Strategy Call</h1>
            <p>Use this call to review your agency gaps, revenue leakage, and implementation options.</p>

            <form method='post' action='/book-call/submit' style='display:grid;gap:12px;'>
                <input name='name' placeholder='Your Name' required style='padding:14px;border:1px solid #ddd;border-radius:10px;'>
                <input name='email' type='email' placeholder='Email Address' required style='padding:14px;border:1px solid #ddd;border-radius:10px;'>
                <input name='agency' placeholder='Agency Name' style='padding:14px;border:1px solid #ddd;border-radius:10px;'>
                <input name='phone' placeholder='Phone Number' style='padding:14px;border:1px solid #ddd;border-radius:10px;'>
                <input name='preferred_time' placeholder='Preferred Day/Time' style='padding:14px;border:1px solid #ddd;border-radius:10px;'>
                <textarea name='notes' placeholder='What do you want help fixing?' style='padding:14px;border:1px solid #ddd;border-radius:10px;'></textarea>

                <button style='background:#16a34a;color:white;padding:15px;border:none;border-radius:12px;font-weight:bold;font-size:16px;'>
                    Request Strategy Call
                </button>
            </form>

            <hr>
            <a href='/consulting-checkout' style='display:block;background:#dc2626;color:white;padding:16px;border-radius:12px;text-align:center;text-decoration:none;font-weight:bold;'>
                Skip Call — Start Implementation Now ($2,999)
            </a>
        </div>
    </body>
    </html>
    """

@router.post("/book-call/submit")
def submit_booking(
    name: str = Form(...),
    email: str = Form(...),
    agency: str = Form(""),
    phone: str = Form(""),
    preferred_time: str = Form(""),
    notes: str = Form("")
):
    save_booking(name,email,agency,phone,preferred_time,notes)
    return RedirectResponse("/book-call/thank-you", status_code=303)

@router.get("/book-call/thank-you", response_class=HTMLResponse)
def booking_thank_you():
    return """
    <html>
    <body style='font-family:Arial;background:#f8fafc;padding:40px;'>
        <div style='max-width:760px;margin:auto;background:white;padding:35px;border-radius:18px;box-shadow:0 8px 24px rgba(0,0,0,.08);'>
            <h1 style='color:#16a34a;'>Strategy Call Request Received</h1>
            <p>Your booking request was saved. Next step: review the agency opportunity and prepare for implementation.</p>
            <a href='/consulting-checkout' style='display:inline-block;background:#dc2626;color:white;padding:14px 20px;border-radius:10px;text-decoration:none;font-weight:bold;'>
                Start Implementation Now — $2,999
            </a>
        </div>
    </body>
    </html>
    """

@router.get("/admin/bookings", response_class=HTMLResponse)
def view_bookings():
    if not os.path.exists(BOOKINGS_FILE):
        return "<h1>No bookings yet.</h1>"

    with open(BOOKINGS_FILE, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    html = "<h1>Consulting Bookings</h1><table border='1' cellpadding='10'><tr><th>Date</th><th>Name</th><th>Email</th><th>Agency</th><th>Phone</th><th>Preferred Time</th><th>Status</th><th>Deal Value</th></tr>"

    for r in rows:
        html += f"<tr><td>{r['created_at']}</td><td>{r['name']}</td><td>{r['email']}</td><td>{r['agency']}</td><td>{r['phone']}</td><td>{r['preferred_time']}</td><td>{r['status']}</td><td>${r['deal_value']}</td></tr>"

    html += "</table>"
    return html
