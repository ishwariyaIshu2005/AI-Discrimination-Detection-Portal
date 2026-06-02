import sqlite3

DB_NAME = "discrimination.db"

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text_content TEXT,
        result TEXT,
        severity INTEGER,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()

def add_default_admin():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=?",
        ("admin",)
    )

    user = cursor.fetchone()

    if not user:
        cursor.execute(
            "INSERT INTO users(username,password) VALUES(?,?)",
            ("admin","admin123")
        )

    conn.commit()
    conn.close()

def verify_login(username,password):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username,password)
    )

    result = cursor.fetchone()

    conn.close()

    return result

def save_analysis(text,result,severity,date):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO history(
        text_content,
        result,
        severity,
        created_at
    )
    VALUES(?,?,?,?)
    """,(text,result,severity,date))

    conn.commit()
    conn.close()

def get_history():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM history
    ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows