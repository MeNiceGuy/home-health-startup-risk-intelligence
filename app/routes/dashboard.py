from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.services.tracking import get_purchases

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/", response_class=HTMLResponse)
def dashboard():
    rows = get_purchases()

    table = ""
    for email, kit, session, file_path, date in rows:
        table += f"""
        <tr>
            <td>{email}</td>
            <td>{kit}</td>
            <td>{date}</td>
            <td><a href="/download-kit?file={file_path}">Download</a></td>
        </tr>
        """

    return f"""
    <html>
    <body style="font-family:Arial;background:#f8fafc;padding:40px;">
        <h1>Boswell Consulting Group Client Dashboard</h1>

        <table border="1" cellpadding="10" style="background:white;border-collapse:collapse;">
            <tr>
                <th>Email</th>
                <th>Purchased Kit</th>
                <th>Date</th>
                <th>Download</th>
            </tr>
            {table}
        </table>

        <br>
        <a href="/kits/">View Kits</a>
    </body>
    </html>
    """
