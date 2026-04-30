from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from app.services.saas_tracking import get_conn, init_db, USE_POSTGRES

router = APIRouter(prefix="/progress", tags=["Progress Tracker"])

TASKS = [
    "Review weakest category from audit",
    "Assign owner for corrective action",
    "Document current workflow",
    "Identify missing checklist or SOP",
    "Install recommended template/kit",
    "Train staff on updated process",
    "Track KPI improvement",
    "Rerun audit after 30 days"
]

def init_progress_db():
    init_db()
    conn = get_conn()
    cur = conn.cursor()
    id_type = "SERIAL PRIMARY KEY" if USE_POSTGRES else "INTEGER PRIMARY KEY AUTOINCREMENT"

    cur.execute(f"""
    CREATE TABLE IF NOT EXISTS progress_tasks (
        id {id_type},
        client_email TEXT,
        task_name TEXT,
        completed INTEGER DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()

def get_tasks(email):
    init_progress_db()
    conn = get_conn()
    cur = conn.cursor()

    placeholder = "%s" if USE_POSTGRES else "?"
    cur.execute(f"SELECT task_name, completed FROM progress_tasks WHERE client_email={placeholder}", (email,))
    rows = cur.fetchall()

    if not rows:
        for task in TASKS:
            cur.execute(
                f"INSERT INTO progress_tasks (client_email, task_name, completed) VALUES ({placeholder}, {placeholder}, 0)",
                (email, task)
            )
        conn.commit()
        cur.execute(f"SELECT task_name, completed FROM progress_tasks WHERE client_email={placeholder}", (email,))
        rows = cur.fetchall()

    conn.close()
    return rows

@router.get("/", response_class=HTMLResponse)
def tracker(email: str = "demo@client.com"):
    rows = get_tasks(email)
    completed = sum(1 for r in rows if int(r[1]) == 1)
    percent = int((completed / len(rows)) * 100) if rows else 0

    task_html = ""
    for task, done in rows:
        checked = "checked" if int(done) == 1 else ""
        task_html += f"""
        <label class="task">
            <input type="checkbox" name="tasks" value="{task}" {checked}>
            {task}
        </label>
        """

    return f"""
    <html>
    <body style="font-family:Arial;background:#f8fafc;padding:40px;">
    <div style="max-width:900px;margin:auto;background:white;padding:30px;border-radius:18px;">
    <h1>30-Day Execution Progress Tracker</h1>
    <p><strong>Client:</strong> {email}</p>
    <h2>Progress: {percent}%</h2>

    <div style="background:#e5e7eb;border-radius:999px;height:24px;">
      <div style="background:#16a34a;width:{percent}%;height:24px;border-radius:999px;"></div>
    </div>

    <form method="post" action="/progress/save">
      <input type="hidden" name="email" value="{email}">
      <div style="margin-top:25px;">{task_html}</div>
      <button style="margin-top:20px;background:#2563eb;color:white;padding:14px 20px;border:0;border-radius:10px;">
      Save Progress
      </button>
    </form>
    </div>
    </body>
    </html>
    """

@router.post("/save")
def save_progress(email: str = Form(...), tasks: list[str] = Form([])):
    init_progress_db()
    conn = get_conn()
    cur = conn.cursor()
    placeholder = "%s" if USE_POSTGRES else "?"

    cur.execute(f"UPDATE progress_tasks SET completed=0 WHERE client_email={placeholder}", (email,))

    for task in tasks:
        cur.execute(
            f"UPDATE progress_tasks SET completed=1 WHERE client_email={placeholder} AND task_name={placeholder}",
            (email, task)
        )

    conn.commit()
    conn.close()

    return RedirectResponse(f"/progress/?email={email}", status_code=303)


