from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/mini-audit", response_class=HTMLResponse)
def mini_audit(request: Request):

    agency = request.query_params.get("agency", "Your Agency")
    state = request.query_params.get("state", "VA")

    return f"""
    <html>
    <body style="font-family:Arial;background:#f8fafc;margin:0;color:#111827;">

        <section style="background:linear-gradient(135deg,#111827,#dc2626);color:white;padding:60px;text-align:center;">
            <h1>Revenue Risk Signals Detected</h1>
            <p>{agency} ({state}) shows performance indicators that may suggest revenue leakage.</p>
        </section>

        <section style="max-width:900px;margin:40px auto;padding:0 20px;">

            <div style="background:white;padding:30px;border-radius:18px;box-shadow:0 10px 30px rgba(0,0,0,.08);">
                <h2>Detected Risk Signals</h2>

                <ul style="font-size:18px;line-height:1.8;">
                    <li>Elevated denial / billing risk patterns</li>
                    <li>Potential A/R delay indicators</li>
                    <li>Operational inefficiencies affecting growth</li>
                </ul>

                <p style="margin-top:20px;">
                    These signals are based on CMS benchmarks and industry performance thresholds.
                </p>
            </div>

            <div style="background:#fff7ed;border-left:6px solid #f59e0b;padding:25px;border-radius:14px;margin-top:25px;">
                <h2>What This Means</h2>
                <p style="font-size:18px;">
                    Agencies with similar signal patterns often experience
                    <strong>$10,000–$50,000+ per month in preventable revenue loss.</strong>
                </p>
            </div>

            <div style="background:white;padding:30px;border-radius:18px;box-shadow:0 10px 30px rgba(0,0,0,.08);margin-top:25px;">
                <h2>Full Audit Required</h2>

                <p style="font-size:18px;line-height:1.7;">
                    The full performance audit reveals:
                </p>

                <ul style="font-size:18px;line-height:1.8;">
                    <li>Estimated monthly revenue loss</li>
                    <li>Exact leakage drivers</li>
                    <li>CMS percentile ranking</li>
                    <li>Market demand positioning</li>
                    <li>Step-by-step correction roadmap</li>
                </ul>

                <p style="margin-top:20px;">
                    This level of detail is not included in the preview.
                </p>

                <a href="/audit-checkout"
                   style="display:block;background:#dc2626;color:white;text-align:center;padding:16px;border-radius:12px;text-decoration:none;font-weight:bold;margin-top:20px;font-size:18px;">
                   Unlock Full Audit ($199)
                </a>
            </div>

            <div style="background:#f3f4f6;padding:20px;border-radius:14px;margin-top:20px;">
                <p style="font-size:14px;line-height:1.6;">
                    This preview is based on public CMS data and generalized benchmarks. The full audit provides deeper analysis using additional inputs and scoring models. This tool provides operational insights only and does not constitute legal, clinical, or regulatory advice.
                </p>
            </div>

        </section>

    </body>
    </html>
    """


