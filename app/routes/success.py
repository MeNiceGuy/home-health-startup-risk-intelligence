from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/success", response_class=HTMLResponse)
def success():
    return """
    <html>
    <head>
        <title>Payment Successful</title>
    </head>
    <body>
        <h1>Payment Successful</h1>
        <p>Your Startup Risk Audit has been unlocked.</p>
        <a href="/audit/">Start Your Audit</a>
    </body>
    </html>
    """
