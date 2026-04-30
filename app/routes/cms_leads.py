from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.services.cms_lead_targeting import build_targets, add_targets_to_outreach_queue

router = APIRouter()

@router.get("/admin/cms-leads", response_class=HTMLResponse)
def cms_leads():
    return """
    <html>
    <body style='font-family:Arial;background:#f8fafc;padding:40px;'>
    <div style='max-width:900px;margin:auto;background:white;padding:35px;border-radius:18px;box-shadow:0 10px 30px rgba(0,0,0,.08);'>
        <h1>CMS High-Probability Lead Targeting</h1>
        <p>Score CMS agencies by public performance signals and export prospects for outreach.</p>

        <a href='/admin/cms-leads/run?limit=250'
           style='display:inline-block;background:#dc2626;color:white;padding:14px 22px;border-radius:12px;text-decoration:none;font-weight:bold;'>
           Build Target List
        </a>

        <a href='/admin/cms-leads/queue'
           style='display:inline-block;background:#111827;color:white;padding:14px 22px;border-radius:12px;text-decoration:none;font-weight:bold;margin-left:10px;'>
           Add Targets to Outreach Queue
        </a>

        <p style='margin-top:25px;color:#6b7280;'>
        Note: Email addresses are not included in CMS data. Add verified business emails before sending outreach.
        </p>
    </div>
    </body>
    </html>
    """

@router.get("/admin/cms-leads/run", response_class=HTMLResponse)
def run_cms_leads(limit: int = 250, state: str = ""):
    result = build_targets(limit=limit, state_filter=state)

    return f"""
    <html>
    <body style='font-family:Arial;background:#f8fafc;padding:40px;'>
    <div style='max-width:900px;margin:auto;background:white;padding:35px;border-radius:18px;box-shadow:0 10px 30px rgba(0,0,0,.08);'>
        <h1>Targeting Complete</h1>
        <p><strong>Targets created:</strong> {result.get("created",0)}</p>
        <p><strong>Export file:</strong> {result.get("file","N/A")}</p>
        <p>{result.get("error","")}</p>
        <a href='/admin/cms-leads'>Back</a>
    </div>
    </body>
    </html>
    """

@router.get("/admin/cms-leads/queue", response_class=HTMLResponse)
def queue_cms_leads():
    result = add_targets_to_outreach_queue()

    return f"""
    <html>
    <body style='font-family:Arial;background:#f8fafc;padding:40px;'>
    <div style='max-width:900px;margin:auto;background:white;padding:35px;border-radius:18px;box-shadow:0 10px 30px rgba(0,0,0,.08);'>
        <h1>Outreach Queue Updated</h1>
        <p><strong>New leads added:</strong> {result.get("added",0)}</p>
        <p>{result.get("error","")}</p>
        <a href='/admin/outreach'>View Outreach Dashboard</a>
    </div>
    </body>
    </html>
    """

