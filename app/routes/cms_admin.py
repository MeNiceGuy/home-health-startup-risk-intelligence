from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.services.cms_data import download_cms_files, cms_status, find_agency_by_name_state

router = APIRouter()

@router.get("/admin/cms/status", response_class=HTMLResponse)
def cms_status_page():
    status = cms_status()

    html = "<h1>CMS Data Status</h1><table border='1' cellpadding='10'><tr><th>Dataset</th><th>Exists</th><th>Path</th></tr>"

    for name, item in status.items():
        html += f"<tr><td>{name}</td><td>{item['exists']}</td><td>{item['path']}</td></tr>"

    html += "</table><br><a href='/admin/cms/download'>Download/Refresh CMS Data</a>"
    return html

@router.get("/admin/cms/download", response_class=HTMLResponse)
def cms_download_page():
    results = download_cms_files()

    html = "<h1>CMS Download Results</h1><table border='1' cellpadding='10'><tr><th>Dataset</th><th>Status</th><th>Details</th></tr>"

    for r in results:
        html += f"<tr><td>{r.get('dataset')}</td><td>{r.get('status')}</td><td>{r.get('path', r.get('error',''))}</td></tr>"

    html += "</table><br><a href='/admin/cms/status'>Back to CMS Status</a>"
    return html

@router.get("/admin/cms/search", response_class=HTMLResponse)
def cms_search_page(agency: str = "", state: str = ""):
    matches = find_agency_by_name_state(agency, state)

    html = f"<h1>CMS Agency Search</h1><p>Agency: {agency} | State: {state}</p>"

    if not matches:
        html += "<p>No matches found. Make sure CMS data is downloaded first.</p>"
    else:
        html += "<table border='1' cellpadding='8'>"
        for row in matches:
            html += "<tr>"
            for k, v in list(row.items())[:12]:
                html += f"<td><strong>{k}</strong><br>{v}</td>"
            html += "</tr>"
        html += "</table>"

    return html



