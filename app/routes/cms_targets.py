from fastapi import APIRouter
from fastapi.responses import HTMLResponse, FileResponse
from app.services.cms_targeting import build_target_list, EXPORT_FILE

router = APIRouter()

@router.get("/admin/cms/targets", response_class=HTMLResponse)
def cms_targets():
    targets = build_target_list(100)

    html = "<h1>CMS Target Agencies</h1>"
    html += "<p>Agencies ranked by public CMS performance signals.</p>"
    html += "<a href='/admin/cms/targets/export'>Download CSV Export</a><br><br>"
    html += "<table border='1' cellpadding='8'>"

    for row in targets[:50]:
        html += f"<tr><td>{row.get('_lead_score')}</td><td>{row.get('Provider Name', row.get('provider_name','Unknown'))}</td><td>{row.get('State','')}</td><td>{row.get('_signals')}</td><td><a href='/mini-audit?agency={row.get('Provider Name','')}&state={row.get('State','')}'>Preview</a></td></tr>"

    html += "</table>"
    return html

@router.get("/admin/cms/targets/export")
def export_targets():
    build_target_list(500)
    return FileResponse(EXPORT_FILE, filename="target_agencies.csv")


