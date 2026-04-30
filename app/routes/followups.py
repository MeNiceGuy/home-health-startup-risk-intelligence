from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.services.followup_engine import send_multi_stage_followups

router = APIRouter()

@router.get("/admin/followups", response_class=HTMLResponse)
def followup_dashboard():
    return """
    <html>
    <body style='font-family:Arial;background:#f8fafc;padding:40px;'>
        <div style='max-width:850px;margin:auto;background:white;padding:35px;border-radius:18px;box-shadow:0 10px 30px rgba(0,0,0,.08);'>
            <h1>Automated Follow-Up Sequence</h1>
            <p>This sends the next eligible follow-up stage to leads who clicked the preview or started checkout but did not purchase.</p>

            <div style='display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:25px 0;'>
                <div style='background:#f9fafb;padding:18px;border-radius:14px;'>
                    <h3>Day 1</h3>
                    <p>Incomplete preview reminder.</p>
                </div>
                <div style='background:#fff7ed;padding:18px;border-radius:14px;'>
                    <h3>Day 2</h3>
                    <p>Revenue-risk escalation.</p>
                </div>
                <div style='background:#fee2e2;padding:18px;border-radius:14px;'>
                    <h3>Day 3</h3>
                    <p>Final action reminder.</p>
                </div>
            </div>

            <a href='/admin/followups/send'
               style='display:inline-block;background:#dc2626;color:white;padding:14px 22px;border-radius:12px;text-decoration:none;font-weight:bold;'>
               Send Next Follow-Up Stage
            </a>
        </div>
    </body>
    </html>
    """

@router.get("/admin/followups/send", response_class=HTMLResponse)
def send_followups():
    result = send_multi_stage_followups()
    return f"""
    <html>
    <body style='font-family:Arial;background:#f8fafc;padding:40px;'>
        <div style='max-width:850px;margin:auto;background:white;padding:35px;border-radius:18px;box-shadow:0 10px 30px rgba(0,0,0,.08);'>
            <h1>Follow-Up Results</h1>
            <p><strong>Emails sent:</strong> {result.get("sent",0)}</p>
            <p><strong>Skipped:</strong> {result.get("skipped",0)}</p>
            <a href='/admin/followups'>Back</a>
        </div>
    </body>
    </html>
    """

