from fastapi import APIRouter, Query
from fastapi.responses import HTMLResponse
from app.services.compliance_engine import get_state_rules

router = APIRouter(prefix="/launch", tags=["Launch"])

@router.get("/{state}", response_class=HTMLResponse)
def launch_dashboard(state: str, completed: str = Query("")):
    data = get_state_rules(state)

    completed_items = completed.split(",") if completed else []

    steps_html = ""
    completed_count = 0

    for step in data["launch_steps"]:
        checked = "checked" if step in completed_items else ""
        if step in completed_items:
            completed_count += 1

        steps_html += f"""
        <li>
            <input type="checkbox" {checked} onchange="updateProgress()">
            {step}
        </li>
        """

    total_steps = len(data["launch_steps"])
    percent = int((completed_count / total_steps) * 100) if total_steps else 0

    compliance_html = "".join([f"<li>{item}</li>" for item in data["compliance_categories"]])
    risk_html = "".join([f"<li>{item}</li>" for item in data["risk_flags"]])

    return f"""
    <html>
    <head>
        <title>{data["state"]} Dashboard</title>
        <style>
            body {{ font-family: Arial; background:#f4f6f8; padding:40px; }}
            .card {{ background:white; padding:30px; max-width:900px; margin:auto; border-radius:12px; box-shadow:0 4px 14px rgba(0,0,0,.08); }}
            h1 {{ margin-bottom:10px; }}
            .progress {{ font-size:24px; margin-bottom:20px; }}
            ul {{ margin-bottom:20px; }}
            a {{ display:inline-block; padding:10px 15px; background:#2563eb; color:white; text-decoration:none; border-radius:8px; }}
        </style>

        <script>
        function updateProgress() {{
            let checkboxes = document.querySelectorAll("input[type=checkbox]");
            let completed = [];

            checkboxes.forEach((cb, index) => {{
                if (cb.checked) {{
                    completed.push(cb.parentElement.innerText.trim());
                }}
            }});

            let query = completed.join(",");
            window.location.href = "/launch/virginia?completed=" + encodeURIComponent(query);
        }}
        </script>

    </head>
    <body>
        <div class="card">
            <h1>{data["state"]} Home Health Launch Dashboard</h1>

            <div class="progress">
                Startup Readiness: <strong>{percent}%</strong>
            </div>

            <h2>Launch Steps</h2>
            <ul>{steps_html}</ul>

            <h2>Compliance Categories</h2>
            <ul>{compliance_html}</ul>

            <h2>Common Risk Flags</h2>
            <ul>{risk_html}</ul>

            <a href="/audit/">Run Compliance Audit</a>
        </div>
    </body>
    </html>
    """


