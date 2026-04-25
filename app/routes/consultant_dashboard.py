from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from pathlib import Path
from datetime import datetime
from app.services.saas_tracking import get_conn, init_db, USE_POSTGRES

router = APIRouter(prefix="/consultant", tags=["Consultant Dashboard"])

UPLOAD_DIR = Path("consultant_uploads")
REPORT_DIR = Path("consultant_reports")
UPLOAD_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)

def init_consultant_db():
    init_db()
    conn = get_conn()
    cur = conn.cursor()
    id_type = "SERIAL PRIMARY KEY" if USE_POSTGRES else "INTEGER PRIMARY KEY AUTOINCREMENT"

    cur.execute(f"""
    CREATE TABLE IF NOT EXISTS consultant_clients (
        id {id_type},
        tenant TEXT,
        client_name TEXT,
        client_email TEXT,
        client_stage TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute(f"""
    CREATE TABLE IF NOT EXISTS consultant_uploads (
        id {id_type},
        tenant TEXT,
        client_name TEXT,
        filename TEXT,
        filepath TEXT,
        report TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def db_placeholder():
    return "%s" if USE_POSTGRES else "?"

def get_metrics(tenant):
    init_consultant_db()
    conn = get_conn()
    cur = conn.cursor()
    p = db_placeholder()

    cur.execute(f"SELECT COUNT(*) FROM consultant_clients WHERE tenant={p}", (tenant,))
    clients_count = cur.fetchone()[0]

    cur.execute(f"SELECT COUNT(*) FROM consultant_uploads WHERE tenant={p}", (tenant,))
    uploads_count = cur.fetchone()[0]

    try:
        cur.execute("SELECT COUNT(*) FROM purchases WHERE status='paid'")
        docs_sold = cur.fetchone()[0]
    except Exception:
        docs_sold = 0

    revenue = docs_sold * 199

    cur.execute(f"""
        SELECT client_name, client_email, client_stage, created_at
        FROM consultant_clients
        WHERE tenant={p}
        ORDER BY id DESC
        LIMIT 10
    """, (tenant,))
    clients = cur.fetchall()

    cur.execute(f"""
        SELECT id, client_name, filename, created_at
        FROM consultant_uploads
        WHERE tenant={p}
        ORDER BY id DESC
        LIMIT 10
    """, (tenant,))
    uploads = cur.fetchall()

    conn.close()
    return clients_count, uploads_count, docs_sold, revenue, clients, uploads

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(tenant: str = "demo"):
    clients_count, uploads_count, docs_sold, revenue, clients, uploads = get_metrics(tenant)

    client_rows = ""
    for c in clients:
        client_rows += f"""
        <tr>
            <td>{c[0]}</td><td>{c[1]}</td><td>{c[2]}</td><td>{str(c[3])[:10]}</td>
            <td><a href="/operating-audit/?tenant={tenant}&client={c[0]}">Run Audit</a></td>
        </tr>
        """
    if not client_rows:
        client_rows = "<tr><td colspan='5'>No clients added yet.</td></tr>"

    upload_rows = ""
    for u in uploads:
        upload_rows += f"""
        <tr>
            <td>{u[1]}</td><td>{u[2]}</td><td>{str(u[3])[:10]}</td>
            <td><a href="/consultant/file-report/{u[0]}?tenant={tenant}">View Report</a></td>
        </tr>
        """
    if not upload_rows:
        upload_rows = "<tr><td colspan='4'>No files uploaded yet.</td></tr>"

    return f"""
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
    body{{margin:0;font-family:Arial;background:#f8fafc;color:#0f172a;}}
    .side{{position:fixed;left:0;top:0;width:240px;height:100vh;background:#0f172a;color:white;padding:24px;}}
    .side a{{display:block;color:#cbd5e1;margin:18px 0;text-decoration:none;}}
    .main{{margin-left:290px;padding:30px;}}
    .grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;}}
    .card{{background:white;padding:24px;border-radius:18px;box-shadow:0 12px 28px rgba(15,23,42,.10);margin-bottom:22px;}}
    .metric{{font-size:34px;font-weight:bold;}}
    .btn{{display:inline-block;background:#2563eb;color:white;padding:12px 16px;border-radius:10px;text-decoration:none;font-weight:bold;margin:6px 6px 0 0;}}
    input,select{{width:100%;padding:12px;border:1px solid #cbd5e1;border-radius:10px;margin-bottom:12px;}}
    button{{background:#16a34a;color:white;padding:13px 18px;border:0;border-radius:10px;font-weight:bold;}}
    table{{width:100%;border-collapse:collapse;}}
    th,td{{padding:12px;border-bottom:1px solid #e5e7eb;text-align:left;}}
    th{{background:#f1f5f9;}}
    @media(max-width:900px){{.side{{position:relative;width:auto;height:auto}}.main{{margin-left:0}}.grid{{grid-template-columns:1fr}}}}
    </style>
    </head>
    <body>
    <div class="side">
      <h2>Consultant Portal</h2>
      <p>{tenant}</p>
      <a href="/consultant/dashboard?tenant={tenant}">Dashboard</a>
      <a href="/operating-audit/?tenant={tenant}">Operating Audit</a>
      <a href="/audit/?tenant={tenant}">Startup Audit</a>
      <a href="/progress/?email=demo@client.com">Progress Tracker</a>
    </div>

    <div class="main">
      <h1>White-Label Consultant Command Center</h1>
      <p>Manage clients, upload business files, run audits, generate reports, and track revenue activity.</p>

      <div class="grid">
        <div class="card"><h3>Total Clients</h3><div class="metric">{clients_count}</div></div>
        <div class="card"><h3>Uploaded Files</h3><div class="metric">{uploads_count}</div></div>
        <div class="card"><h3>Documents Sold</h3><div class="metric">{docs_sold}</div></div>
        <div class="card"><h3>Estimated Revenue</h3><div class="metric">${revenue}</div></div>
      </div>

      <div class="card">
        <h2>Add Client</h2>
        <form method="post" action="/consultant/add-client">
          <input name="tenant" value="{tenant}" type="hidden">
          <input name="client_name" placeholder="Client business name" required>
          <input name="client_email" placeholder="Client email">
          <select name="client_stage">
            <option>Startup</option>
            <option>Operating Agency</option>
            <option>Scaling / Optimization</option>
          </select>
          <button>Add Client</button>
        </form>
      </div>

      <div class="card">
        <h2>Client List</h2>
        <table><tr><th>Business</th><th>Email</th><th>Stage</th><th>Added</th><th>Action</th></tr>{client_rows}</table>
      </div>

      <div class="card">
        <h2>Upload Client Business Files</h2>
        <p>Upload policies, billing notes, staffing records, SOPs, compliance docs, or intake forms. The system will create a review report.</p>
        <form method="post" action="/consultant/upload" enctype="multipart/form-data">
          <input name="tenant" value="{tenant}" type="hidden">
          <input name="client_name" placeholder="Client business name" required>
          <input type="file" name="file" required>
          <button>Upload & Generate Report</button>
        </form>
      </div>

      <div class="card">
        <h2>Uploaded File Reports</h2>
        <table><tr><th>Client</th><th>File</th><th>Date</th><th>Report</th></tr>{upload_rows}</table>
      </div>

      <div class="card">
        <h2>Consultant Tools</h2>
        <a class="btn" href="/operating-audit/?tenant={tenant}">Run Operating Audit</a>
        <a class="btn" href="/audit/?tenant={tenant}">Run Startup Audit</a>
        <a class="btn" href="/client/dashboard?email=client@example.com">Open Client Dashboard</a>
      </div>
    </div>
    </body>
    </html>
    """

def generate_basic_file_report(client_name, filename):
    return f"""
    <h2>Business File Review Report</h2>
    <p><strong>Client:</strong> {client_name}</p>
    <p><strong>File:</strong> {filename}</p>

    <h3>Initial Review</h3>
    <p>This file has been logged for consultant review. Use it to evaluate compliance, operations, staffing, billing, documentation, or policy gaps.</p>

    <h3>Recommended Consultant Review Areas</h3>
    <ul>
      <li>Does the document match the client’s current service model?</li>
      <li>Does it identify ownership, workflow steps, and review frequency?</li>
      <li>Does it support compliance readiness and audit defense?</li>
      <li>Does it expose missing SOPs, policies, or workflow controls?</li>
    </ul>

    <h3>Recommended Next Step</h3>
    <p>Run the Operating Audit or Startup Audit for this client, then connect the findings to a tailored kit or improvement roadmap.</p>
    """

@router.post("/upload", response_class=HTMLResponse)
async def upload(tenant: str = Form("demo"), client_name: str = Form("client"), file: UploadFile = File(...)):
    init_consultant_db()
    safe_client = client_name.replace(" ", "_").lower()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{tenant}_{safe_client}_{timestamp}_{file.filename}"
    path = UPLOAD_DIR / filename

    with open(path, "wb") as f:
        f.write(await file.read())

    report = generate_basic_file_report(client_name, filename)

    conn = get_conn()
    cur = conn.cursor()
    p = db_placeholder()
    cur.execute(
        f"INSERT INTO consultant_uploads (tenant, client_name, filename, filepath, report) VALUES ({p}, {p}, {p}, {p}, {p})",
        (tenant, client_name, filename, str(path), report)
    )
    conn.commit()
    conn.close()

    return HTMLResponse(f"<h1>File Uploaded & Report Created</h1><p>{filename}</p><a href='/consultant/dashboard?tenant={tenant}'>Back to Dashboard</a>")

@router.get("/file-report/{file_id}", response_class=HTMLResponse)
def file_report(file_id: int, tenant: str = "demo"):
    init_consultant_db()
    conn = get_conn()
    cur = conn.cursor()
    p = db_placeholder()
    cur.execute(f"SELECT client_name, filename, report FROM consultant_uploads WHERE id={p} AND tenant={p}", (file_id, tenant))
    row = cur.fetchone()
    conn.close()

    if not row:
        return HTMLResponse("<h1>Report not found</h1>", status_code=404)

    return f"""
    <html><body style="font-family:Arial;background:#f8fafc;padding:40px;">
    <div style="max-width:900px;margin:auto;background:white;padding:35px;border-radius:18px;">
    <h1>Uploaded File Intelligence Report</h1>
    <p><strong>Client:</strong> {row[0]}</p>
    <p><strong>File:</strong> {row[1]}</p>
    {row[2]}
    <br><a href="/consultant/dashboard?tenant={tenant}">Back to Dashboard</a>
    </div>
    </body></html>
    """

@router.post("/add-client", response_class=HTMLResponse)
def add_client(tenant: str = Form("demo"), client_name: str = Form(...), client_email: str = Form(""), client_stage: str = Form("")):
    init_consultant_db()
    conn = get_conn()
    cur = conn.cursor()
    p = db_placeholder()
    cur.execute(
        f"INSERT INTO consultant_clients (tenant, client_name, client_email, client_stage) VALUES ({p}, {p}, {p}, {p})",
        (tenant, client_name, client_email, client_stage)
    )
    conn.commit()
    conn.close()

    return HTMLResponse(f"<h1>Client Added</h1><p>{client_name}</p><a href='/consultant/dashboard?tenant={tenant}'>Back to Dashboard</a>")
