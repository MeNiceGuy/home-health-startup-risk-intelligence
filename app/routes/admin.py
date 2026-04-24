from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.services.tracking import init_db, get_purchases

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/purchases", response_class=HTMLResponse)
def purchases():
    init_db()
    rows = get_purchases()

    table_rows = ""

    for email, kit, session, date in rows:
        table_rows += f"""
        <tr>
            <td>{email}</td>
            <td>{kit}</td>
            <td>{date}</td>
            <td>{session}</td>
        </tr>
        """

    return f"""
    <html>
    <body style="font-family:Arial;padding:40px;">
        <h1>Purchase Tracking Dashboard</h1>

        <table border="1" cellpadding="10">
            <tr>
                <th>Email</th>
                <th>Kit</th>
                <th>Date</th>
                <th>Stripe Session</th>
            </tr>
            {table_rows}
        </table>
    </body>
    </html>
    """
