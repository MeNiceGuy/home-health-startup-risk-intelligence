from passlib.hash import bcrypt
from app.services.saas_tracking import get_conn, init_db, USE_POSTGRES

def create_user(email, password):
    init_db()
    conn = get_conn()
    cur = conn.cursor()

    hashed = bcrypt.hash(password)

    if USE_POSTGRES:
        cur.execute(
            "INSERT INTO users (email, password_hash) VALUES (%s, %s)",
            (email, hashed)
        )
    else:
        cur.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            (email, hashed)
        )

    conn.commit()
    conn.close()

def verify_user(email, password):
    init_db()
    conn = get_conn()
    cur = conn.cursor()

    if USE_POSTGRES:
        cur.execute(
            "SELECT id, password_hash FROM users WHERE email=%s",
            (email,)
        )
    else:
        cur.execute(
            "SELECT id, password_hash FROM users WHERE email=?",
            (email,)
        )

    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    user_id, password_hash = row

    if bcrypt.verify(password, password_hash):
        return {"id": user_id, "email": email}

    return None


