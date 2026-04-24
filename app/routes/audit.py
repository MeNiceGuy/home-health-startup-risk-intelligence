from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/audit", tags=["Audit"])

def field(label, name, options, tip):
    opts = "".join([f'<option value="{v}">{t}</option>' for v,t in options])
    return f"""
    <div class="field">
        <label>{label} <span class="tip" data-tip="{tip}">?</span></label>
        <select name="{name}">{opts}</select>
    </div>
    """

@router.get("/", response_class=HTMLResponse)
def audit_form():

    yn = [("no","No"),("yes","Yes")]
    ypn = [("no","No"),("partial","Partial"),("yes","Yes")]

    return f"""
    <html>
    <head>
    <style>
        body {{
            font-family: Arial;
            background:#f8fafc;
            margin:0;
            padding:0;
        }}

        .container {{
            max-width:1100px;
            margin:40px auto;
            padding:20px;
        }}

        .card {{
            background:white;
            padding:25px;
            border-radius:14px;
            margin-bottom:20px;
            box-shadow:0 6px 18px rgba(0,0,0,0.08);
        }}

        h1 {{
            margin-bottom:10px;
        }}

        .grid {{
            display:grid;
            grid-template-columns:1fr 1fr;
            gap:18px;
        }}

        .field label {{
            font-weight:bold;
            display:block;
            margin-bottom:6px;
        }}

        select, input {{
            width:100%;
            padding:10px;
            border-radius:8px;
            border:1px solid #cbd5e1;
        }}

        .tip {{
            background:#2563eb;
            color:white;
            border-radius:50%;
            padding:2px 6px;
            font-size:12px;
            margin-left:6px;
            cursor:pointer;
            position:relative;
        }}

        .tip:hover::after {{
            content:attr(data-tip);
            position:absolute;
            left:20px;
            top:-5px;
            width:260px;
            background:#0f172a;
            color:white;
            padding:10px;
            border-radius:8px;
            font-size:13px;
            z-index:999;
        }}

        button {{
            background:#2563eb;
            color:white;
            padding:14px 20px;
            border:none;
            border-radius:10px;
            font-weight:bold;
            cursor:pointer;
        }}
    </style>
    </head>

    <body>
    <div class="container">

        <div class="card">
            <h1>Boswell Consulting Group Startup Intelligence Audit</h1>
            <p>Diagnose licensing, staffing, compliance, and revenue risks before launch.</p>
        </div>

        <form method="post" action="/audit/run">

            <div class="card">
                <h2>Client Information</h2>
                <div class="grid">
                    <div><label>Agency Name</label><input name="agency_name"></div>
                    <div><label>Owner Name</label><input name="owner_name"></div>
                    <div><label>City / County</label><input name="location"></div>
                    <div><label>Target Start Date</label><input type="date" name="start_date"></div>
                </div>
            </div>

            <div class="card">
                <h2>Licensing</h2>
                <div class="grid">
                    {field("Business Entity Formed?", "business_registered", ypn, "LLC or corporation registered with the state")}
                    {field("EIN Obtained?", "ein_obtained", yn, "Federal tax ID from IRS")}
                    {field("License Type Identified?", "license_type_identified", ypn, "Home care vs home health")}
                    {field("Documents Prepared?", "license_docs_ready", ypn, "All paperwork ready for submission")}
                </div>
            </div>

            <div class="card">
                <h2>Clinical</h2>
                <div class="grid">
                    {field("RN Supervisor Secured?", "rn_secured", [("no","No"),("contracted","Contracted"),("yes","Yes")], "RN required for oversight")}
                    {field("Leadership Qualified?", "clinical_qualified", [("no","No"),("unknown","Unknown"),("yes","Yes")], "Meets state requirements")}
                </div>
            </div>

            <div class="card">
                <h2>Revenue</h2>
                <div class="grid">
                    {field("Payer Strategy?", "revenue_model", [("no","No"),("private","Private Pay"),("medicaid","Medicaid"),("medicare","Medicare")], "How you get paid")}
                    {field("Reimbursement Timeline?", "revenue_timeline", ypn, "When money comes in")}
                </div>
            </div>

            <div class="card">
                <h2>Compliance</h2>
                <div class="grid">
                    {field("Policies Ready?", "policies_ready", ypn, "Required documentation")}
                    {field("HIPAA System?", "hipaa_system", ypn, "Secure patient data handling")}
                </div>
            </div>

            <button type="submit">Run Intelligence Audit</button>

        </form>

    </div>
    </body>
    </html>
    """
