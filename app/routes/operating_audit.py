from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
import json

router = APIRouter(prefix="/operating-audit", tags=["Operating Intelligence"])

def risk_score(value, benchmark, higher_is_bad=True):
    try:
        value = float(value)
        benchmark = float(benchmark)
        if higher_is_bad:
            ratio = value / benchmark if benchmark else 1
        else:
            ratio = benchmark / value if value else 2

        if ratio <= 1:
            return 90
        elif ratio <= 1.25:
            return 75
        elif ratio <= 1.5:
            return 60
        else:
            return 35
    except:
        return 40

@router.get("/", response_class=HTMLResponse)
def form():
    return """
    <html><body style="font-family:Arial;padding:40px;">
    <h1>Operating Intelligence Audit</h1>

    <form method="post" action="/operating-audit/run">
    Days in A/R: <input name="ar_days" value="45"><br>
    Denial Rate (%): <input name="denial_rate" value="15"><br>
    Clean Claim Rate (%): <input name="clean_rate" value="80"><br>
    Intake Time: <input name="intake_time" value="5"><br>
    Documentation Lag: <input name="doc_lag" value="3"><br>
    Missed Visits (%): <input name="missed_visits" value="8"><br>
    Open Roles: <input name="open_roles" value="3"><br>
    Turnover (%): <input name="turnover" value="40"><br>
    QA Score (%): <input name="qa_score" value="75"><br>
    HIPAA Score (%): <input name="hipaa_score" value="85"><br>

    <button type="submit">Run Audit</button>
    </form>
    </body></html>
    """

@router.post("/run", response_class=HTMLResponse)
def run(
    ar_days: float = Form(0),
    denial_rate: float = Form(0),
    clean_rate: float = Form(0),
    intake_time: float = Form(0),
    doc_lag: float = Form(0),
    missed_visits: float = Form(0),
    open_roles: float = Form(0),
    turnover: float = Form(0),
    qa_score: float = Form(0),
    hipaa_score: float = Form(0)
):

    financial = int((risk_score(ar_days,30) + risk_score(denial_rate,10) + risk_score(clean_rate,90,False)) / 3)
    operations = int((risk_score(intake_time,2) + risk_score(doc_lag,1) + risk_score(missed_visits,5)) / 3)
    staffing = int((risk_score(open_roles,1) + risk_score(turnover,30)) / 2)
    compliance = int((risk_score(qa_score,90,False) + risk_score(hipaa_score,95,False)) / 2)

    total = int((financial + operations + staffing + compliance) / 4)

    # FINANCIAL IMPACT
    lost_revenue = int((denial_rate - 10) * 1000) if denial_rate > 10 else 0
    delay_cost = int((ar_days - 30) * 500) if ar_days > 30 else 0
    total_impact = lost_revenue + delay_cost

    # PRIORITY ENGINE
    actions = [
        ("Financial", financial, lost_revenue),
        ("Operations", operations, delay_cost),
        ("Staffing", staffing, 1500),
        ("Compliance", compliance, 2000)
    ]

    actions = sorted(actions, key=lambda x: x[1])

    # ROADMAP
    roadmap_html = ""
    for i, (name, score, impact) in enumerate(actions):
        roadmap_html += f"""
        <div>
        <h3>Week {i+1}: {name}</h3>
        <p>Focus on improving {name}. Estimated impact: ${impact}</p>
        </div>
        """

    return f"""
    <html><body style="font-family:Arial;padding:40px;">
    <h1>Operating Intelligence Report</h1>

    <h2>Total Score: {total}</h2>

    <h2>Financial Impact</h2>
    <p>Revenue Loss: ${lost_revenue}</p>
    <p>Cash Delay: ${delay_cost}</p>

    <h2>30-Day Roadmap</h2>
    {roadmap_html}

    </body></html>
    """
