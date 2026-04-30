from fastapi import APIRouter, Form, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from itsdangerous import URLSafeSerializer
from app.services.users import create_user, verify_user
import os

router = APIRouter(prefix="/auth", tags=["Auth"])

SECRET = os.getenv("APP_SECRET", "dev-secret-change-this")
serializer = URLSafeSerializer(SECRET)

def get_current_user(request: Request):
    cookie = request.cookies.get("session")
    if not cookie:
        return None
    try:
        return serializer.loads(cookie)
    except Exception:
        return None

@router.get("/signup", response_class=HTMLResponse)
def signup_page():
    return """
    <html><body style="font-family:Arial;padding:40px;">
        <h1>Create Account</h1>
        <form method="post" action="/auth/signup">
            Email:<br><input name="email"><br><br>
            Password:<br><input type="password" name="password"><br><br>
            <button type="submit">Sign Up</button>
        </form>
    </body></html>
    """

@router.post("/signup")
def signup(response: Response, email: str = Form(...), password: str = Form(...)):
    create_user(email, password)
    session = serializer.dumps({"email": email})
    resp = RedirectResponse("/dashboard/", status_code=302)
    resp.set_cookie("session", session, httponly=True)
    return resp

@router.get("/login", response_class=HTMLResponse)
def login_page():
    return """
    <html><body style="font-family:Arial;padding:40px;">
        <h1>Login</h1>
        <form method="post" action="/auth/login">
            Email:<br><input name="email"><br><br>
            Password:<br><input type="password" name="password"><br><br>
            <button type="submit">Login</button>
        </form>
    </body></html>
    """

@router.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    user = verify_user(email, password)
    if not user:
        return HTMLResponse("<h1>Invalid login</h1>")

    session = serializer.dumps({"email": email})
    resp = RedirectResponse("/dashboard/", status_code=302)
    resp.set_cookie("session", session, httponly=True)
    return resp

@router.get("/logout")
def logout():
    resp = RedirectResponse("/", status_code=302)
    resp.delete_cookie("session")
    return resp


