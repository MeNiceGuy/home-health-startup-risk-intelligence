import sqlite3
DB="app_data.db"

def migrate():
    con=sqlite3.connect(DB); c=con.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY, email TEXT UNIQUE, password_hash TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS purchases(
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        kit_slug TEXT,
        file_path TEXT,
        created_at TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS intelligence_scores(
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        agency_name TEXT,
        total INTEGER,
        compliance INTEGER,
        clinical INTEGER,
        revenue INTEGER,
        operations INTEGER,
        created_at TEXT
    )""")

    con.commit(); con.close()
