from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/", response_class=HTMLResponse)
def dashboard():
    return """
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
    body{font-family:Arial;background:#f8fafc;padding:20px;}
    .card{background:white;padding:20px;border-radius:12px;margin-bottom:20px;}
    </style>
    </head>

    <body>

    <h1>Operational Intelligence Dashboard</h1>

    <div class="card">
    <h2>Performance Summary</h2>
    <p>
    Your organization is currently operating below industry benchmarks
    in financial, compliance, and staffing performance.
    </p>
    </div>

    <div class="card">
    <h2>Key Bottlenecks</h2>
    <ul>
    <li>Revenue leakage from high denial rates</li>
    <li>Operational delays from intake inefficiency</li>
    <li>Compliance exposure from low QA performance</li>
    </ul>
    </div>

    <div class="card">
    <h2>Industry Comparison</h2>
    <p>
    Compared to industry standards, your agency is performing below
    average across multiple categories, indicating a need for immediate
    system optimization.
    </p>
    </div>

    <div class="card">
    <h2>Recommended Action</h2>
    <p>Fix financial systems, compliance structure, and staffing pipeline immediately.</p>
    </div>

    </body>
    </html>
    """
