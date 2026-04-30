from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/upsell/consulting", response_class=HTMLResponse)
def consulting_offer():
    from app.routes.tracking import track_event
    track_event("upsell_view", "consulting_page")
    return """
    <html>
    <body style='font-family:Arial;background:#f8fafc;padding:40px;'>

    <div style='max-width:850px;margin:auto;background:white;padding:40px;border-radius:18px;box-shadow:0 10px 30px rgba(0,0,0,.1);'>

        <h1 style='font-size:34px;'>Your Agency Is Losing Revenue Every Month</h1>

        <p style='font-size:18px;color:#444;'>
        Most home health agencies unknowingly lose $10K–$50K per year due to operational inefficiencies.
        </p>

        <hr>

        <h2>Where Revenue Is Leaking</h2>
        <ul style='font-size:17px;'>
            <li>Slow intake → missed patient starts</li>
            <li>Denials → lost billing revenue</li>
            <li>Staffing gaps → missed visits</li>
            <li>Poor workflows → operational delays</li>
        </ul>

        <hr>

        <h2>What We Built To Fix It</h2>
        <p style='font-size:17px;'>
        A 14-day implementation system designed specifically for home health agencies to fix revenue leaks and optimize operations.
        </p>

        <ul>
            <li>Full operational audit breakdown</li>
            <li>Revenue recovery system</li>
            <li>Workflow implementation plan</li>
            <li>Denial + AR optimization</li>
            <li>Execution checklist (step-by-step)</li>
        </ul>

        <hr>

        <h2>Expected Outcome</h2>
        <p style='font-size:18px;font-weight:bold;color:#16a34a;'>
        Most agencies recover $15K–$40K within 30–60 days.
        </p>

        <hr>

        <h2>Why This Works</h2>
        <p>
        This system is built specifically for home health operations—not generic consulting advice.
        You are not guessing what to fix—you are following a structured system.
        </p>

        <hr>

        <div style="background:#fee2e2;border-left:6px solid #dc2626;padding:18px;border-radius:12px;margin:25px 0;">
    <h2 style="color:#991b1b;margin-top:0;">Limited Implementation Capacity</h2>
    <p><strong>Only 3 implementation spots are available this week.</strong></p>
    <p>Every month you delay allows revenue leakage, denial issues, staffing gaps, and operational inefficiencies to continue compounding.</p>
</div>

<h2>Investment</h2>
        <h1 style='color:#dc2626;'>$2,999</h1>

        <p>
        If you recover even a fraction of lost revenue, this pays for itself.
        </p>

        <a href="/track?event=consulting_checkout_click&source=consulting_page&redirect=/consulting-checkout"
           style="display:block;background:#dc2626;color:white;padding:18px;border-radius:12px;text-align:center;font-size:20px;font-weight:bold;text-decoration:none;margin-top:20px;">
           Start Implementation Now
        </a>

        <hr>

        <h3>Common Questions</h3>

        <p><strong>Will this work for my agency?</strong><br>
        Yes. This system is built specifically for home health agencies operating under real constraints.</p>

        <p><strong>What if I don’t implement correctly?</strong><br>
        The system provides step-by-step execution guidance.</p>

        <p><strong>Is this worth $2,999?</strong><br>
        If you recover even 10% of lost revenue, it pays for itself quickly.</p>

        <br>

        <a href='/consultant/dashboard?tenant=demo'>Return to Dashboard</a>

    </div>

    </body>
    </html>
    """




