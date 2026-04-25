from passlib.hash import bcrypt
from app.services.saas_tracking import get_conn, init_db

def init_users_db():
    init_db()

def create_user(email, password):
    init_db()
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (email, password_hash) VALUES (%s, %s)",
                (email, bcrypt.hash(password))
            )
            conn.commit()

def verify_user(email, password):
    init_db()
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, password_hash FROM users WHERE email=%s", (email,))
            row = cur.fetchone()

    if not row:
        return None

    user_id, password_hash = row
    if bcrypt.verify(password, password_hash):
        return {"id": user_id, "email": email}

    return None
