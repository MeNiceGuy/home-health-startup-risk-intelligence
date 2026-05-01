from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

from app.services.cms_lead_targeting import build_targets, add_targets_to_outreach_queue
from app.services.lead_enrichment import enrich_targets
from app.services.auto_outreach import send_enriched_outreach
from app.services.followup_engine import send_multi_stage_followups

router = APIRouter()
security = HTTPBasic()

def require_admin(credentials: HTTPBasicCredentials = Depends(security)):
    good_user = secrets.compare_digest(credentials.username, "Admin")
    good_pass = secrets.compare_digest(credentials.password, "Boswell05")

    if not (good_user and good_pass):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid control center login",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True

@router.get("/control-center", response_class=HTMLResponse)
def control_center(_: bool = Depends(require_admin)):
    return """
    <html>
    <body style='font-family:Arial;background:#f8fafc;margin:0;padding:40px;color:#111827;'>
    <div style='max-width:1000px;margin:auto;background:white;padding:35px;border-radius:22px;box-shadow:0 10px 35px rgba(0,0,0,.08);'>
        <h1>Control Center</h1>
        <p>Activate AutoPilot to identify high-risk CMS agency targets, enrich verified emails, send outreach, and trigger follow-ups.</p>

        <div style='display:grid;grid-template-columns:repeat(2,1fr);gap:18px;margin-top:25px;'>
            <a href='/control-center/run-targeting' style='background:#dc2626;color:white;padding:20px;border-radius:14px;text-decoration:none;font-weight:bold;'>1. Build High-Risk CMS Targets</a>
            <a href='/control-center/enrich' style='background:#111827;color:white;padding:20px;border-radius:14px;text-decoration:none;font-weight:bold;'>2. Enrich Verified Emails</a>
            <a href='/control-center/send' style='background:#16a34a;color:white;padding:20px;border-radius:14px;text-decoration:none;font-weight:bold;'>3. Send Outreach</a>
            <a href='/control-center/followups' style='background:#f59e0b;color:#111827;padding:20px;border-radius:14px;text-decoration:none;font-weight:bold;'>4. Send Follow-Ups</a>
        </div>

        <div style='margin-top:30px;background:#fff7ed;padding:22px;border-radius:16px;'>
            <h2>One-Click AutoPilot</h2>
            <p>Runs targeting, queueing, enrichment, outreach, and follow-ups in sequence.</p>
            <a href='/control-center/run-all' style='display:inline-block;background:#dc2626;color:white;padding:16px 26px;border-radius:12px;text-decoration:none;font-weight:bold;'>Run AutoPilot Now</a>
        </div>
    </div>
    </body>
    </html>
    """

@router.get("/control-center/run-targeting", response_class=HTMLResponse)
def run_targeting(_: bool = Depends(require_admin)):
    return result_page("CMS Targeting Complete", build_targets(limit=250))

@router.get("/control-center/enrich", response_class=HTMLResponse)
def run_enrich(_: bool = Depends(require_admin)):
    return result_page("Email Enrichment Complete", enrich_targets())

@router.get("/control-center/send", response_class=HTMLResponse)
def run_send(_: bool = Depends(require_admin)):
    return result_page("Outreach Sent", send_enriched_outreach())

@router.get("/control-center/followups", response_class=HTMLResponse)
def run_followups(_: bool = Depends(require_admin)):
    return result_page("Follow-Ups Sent", send_multi_stage_followups())

@router.get("/control-center/run-all", response_class=HTMLResponse)
def run_all(_: bool = Depends(require_admin)):
    targeting = build_targets(limit=250)
    queue = add_targets_to_outreach_queue()
    enrichment = enrich_targets()
    outreach = send_enriched_outreach()
    followups = send_multi_stage_followups()

    return f"""
    <html><body style='font-family:Arial;background:#f8fafc;padding:40px;'>
    <div style='max-width:900px;margin:auto;background:white;padding:35px;border-radius:22px;'>
        <h1>AutoPilot Run Complete</h1>
        <p><strong>Targets Created:</strong> {targeting.get("created",0)}</p>
        <p><strong>Queued:</strong> {queue.get("added",0)}</p>
        <p><strong>Emails Enriched:</strong> {enrichment.get("updated",0)}</p>
        <p><strong>Outreach Sent:</strong> {outreach.get("sent",0)}</p>
        <p><strong>Follow-Ups Sent:</strong> {followups.get("sent",0)}</p>
        <a href='/control-center'>Back to Control Center</a>
    </div></body></html>
    """

def result_page(title, result):
    return f"""
    <html><body style='font-family:Arial;background:#f8fafc;padding:40px;'>
    <div style='max-width:850px;margin:auto;background:white;padding:35px;border-radius:22px;'>
        <h1>{title}</h1>
        <pre style='background:#f3f4f6;padding:18px;border-radius:12px;white-space:pre-wrap;'>{result}</pre>
        <a href='/control-center'>Back to Control Center</a>
    </div></body></html>
    """
