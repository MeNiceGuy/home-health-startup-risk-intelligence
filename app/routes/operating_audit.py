from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/operating-audit", tags=["Operating Intelligence"])

@router.get("/", response_class=HTMLResponse)
def form():
    return """
    <html>
    <body style="font-family:Arial;padding:40px;">

    <h1>Operating Intelligence Audit</h1>

    <form method="post" action="/operating-audit/run">

    <h2>Financial Performance</h2>
    Days in A/R: <input name="ar_days"><br>
    Claim Denial Rate (%): <input name="denial_rate"><br>
    Clean Claim Rate (%): <input name="clean_rate"><br>

    <h2>Operations</h2>
    Intake Time (days): <input name="intake_time"><br>
    Documentation Lag (days): <input name="doc_lag"><br>
    Missed Visits (%): <input name="missed_visits"><br>

    <h2>Staffing</h2>
    Open Positions: <input name="open_roles"><br>
    Turnover Rate (%): <input name="turnover"><br>

    <h2>Compliance</h2>
    QA Audit Score (%): <input name="qa_score"><br>
    HIPAA Compliance Score (%): <input name="hipaa_score"><br>

    <br><button type="submit">Run Intelligence Audit</button>

    </form>
    </body>
    </html>
    """

@router.post("/run", response_class=HTMLResponse)
def run(
    ar_days:int=Form(0),
    denial_rate:int=Form(0),
    clean_rate:int=Form(0),
    intake_time:int=Form(0),
    doc_lag:int=Form(0),
    missed_visits:int=Form(0),
    open_roles:int=Form(0),
    turnover:int=Form(0),
    qa_score:int=Form(0),
    hipaa_score:int=Form(0)
):

    # INDUSTRY BENCHMARKS
    benchmarks = {
        "ar_days": 30,
        "denial_rate": 10,
        "clean_rate": 90,
        "intake_time": 2,
        "doc_lag": 1,
        "missed_visits": 5,
        "turnover": 30,
        "qa_score": 90,
        "hipaa_score": 95
    }

    return f"""
    <html>
    <body style="font-family:Arial;padding:40px;">
    
    <h1>Operating Intelligence Report</h1>

    <h2>Benchmark Comparison</h2>

    <ul>
    <li>A/R Days: {ar_days} (Industry: {benchmarks['ar_days']})</li>
    <li>Denial Rate: {denial_rate}% (Industry: {benchmarks['denial_rate']}%)</li>
    <li>Clean Claim Rate: {clean_rate}% (Industry: {benchmarks['clean_rate']}%)</li>
    <li>Intake Time: {intake_time} days (Industry: {benchmarks['intake_time']})</li>
    <li>Documentation Lag: {doc_lag} days (Industry: {benchmarks['doc_lag']})</li>
    <li>Missed Visits: {missed_visits}% (Industry: {benchmarks['missed_visits']}%)</li>
    <li>Turnover: {turnover}% (Industry: {benchmarks['turnover']}%)</li>
    <li>QA Score: {qa_score}% (Industry: {benchmarks['qa_score']}%)</li>
    <li>HIPAA Score: {hipaa_score}% (Industry: {benchmarks['hipaa_score']}%)</li>
    </ul>

    <h2>What This Means</h2>
    <p>
    Any metric outside industry benchmark indicates operational inefficiency,
    compliance risk, or revenue leakage.
    </p>

    <a href="/dashboard/">View Intelligence Dashboard</a>

    </body>
    </html>
    """
