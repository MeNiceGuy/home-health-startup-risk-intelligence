from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.services.lead_enrichment import enrich_targets
from app.services.auto_outreach import send_enriched_outreach

router = APIRouter()

@router.get("/admin/enrichment", response_class=HTMLResponse)
def enrichment_home():
    return """
    <html><body style='font-family:Arial;background:#f8fafc;padding:40px;'>
    <div style='max-width:850px;margin:auto;background:white;padding:35px;border-radius:18px;'>
        <h1>Email Enrichment + Auto Outreach</h1>
        <p>Match verified emails to CMS target leads, then send outreach automatically.</p>
        <a href='/admin/enrichment/run'>Enrich Leads</a><br><br>
        <a href='/admin/enrichment/send'>Send Outreach</a>
    </div>
    </body></html>
    """

@router.get("/admin/enrichment/run", response_class=HTMLResponse)
def run_enrichment():
    result = enrich_targets()
    return f"<h1>Enrichment Complete</h1><p>Updated: {result.get('updated',0)}</p><p>{result.get('error','')}</p>"

@router.get("/admin/enrichment/send", response_class=HTMLResponse)
def run_send():
    result = send_enriched_outreach()
    return f"<h1>Outreach Sent</h1><p>Sent: {result.get('sent',0)}</p><p>{result.get('error','')}</p>"

