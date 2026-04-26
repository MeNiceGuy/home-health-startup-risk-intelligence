from fastapi import APIRouter, Query
from fastapi.responses import HTMLResponse
from app.services.client_timeline import get_client_timeline, init_timeline_db

router = APIRouter(prefix="/consultant", tags=["Client Timeline"])

@router.get("/client/{client_name}", response_class=HTMLResponse)
def client_timeline(client_name: str, tenant: str = Query("demo")):
    init_timeline_db()
    events = get_client_timeline(tenant, client_name)

    event_html = ""
    for event_type, title, detail, link, created_at in events:
        action = f'<a href="{link}" style="color:#2563eb;font-weight:bold;">Open</a>' if link else ""
        event_html += f"""
        <div class="event">
            <div class="badge">{event_type}</div>
            <h3>{title}</h3>
            <p>{detail}</p>
            <small>{created_at}</small><br>
            {action}
        </div>
        """

    if not event_html:
        event_html = "<p>No timeline events yet. Upload a file, run an audit, or add a report to begin building client intelligence history.</p>"

    return f"""
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
    body{{font-family:Arial;background:#f8fafc;color:#0f172a;margin:0;padding:40px;}}
    .wrap{{max-width:950px;margin:auto;}}
    .card,.event{{background:white;padding:24px;border-radius:18px;box-shadow:0 12px 28px rgba(15,23,42,.10);margin-bottom:18px;}}
    .badge{{display:inline-block;background:#eff6ff;color:#1d4ed8;padding:7px 12px;border-radius:999px;font-weight:bold;font-size:13px;}}
    .btn{{display:inline-block;background:#2563eb;color:white;padding:12px 16px;border-radius:10px;text-decoration:none;font-weight:bold;margin-right:8px;}}
    </style>
    </head>
    <body>
    <div class="wrap">
        <div class="card">
            <h1>Client Intelligence Timeline</h1>
            <p><strong>Client:</strong> {client_name}</p>
            <p><strong>Tenant:</strong> {tenant}</p>

            <a class="btn" href="/consultant/dashboard?tenant={tenant}">Back to Dashboard</a>
            <a class="btn" href="/operating-audit/?tenant={tenant}&client={client_name}">Run Operating Audit</a>
            <a class="btn" href="/progress/?email={client_name}">Open Progress Tracker</a>
        </div>

        {event_html}
    </div>
    </body>
    </html>
    """
