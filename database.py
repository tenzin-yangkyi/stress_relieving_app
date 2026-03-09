import sqlite3
from datetime import datetime


# Create tables
def create_table():
    conn = sqlite3.connect("journal.db")
    c = conn.cursor()

    # Journal table (linked to username)
    c.execute("""
        CREATE TABLE IF NOT EXISTS journal(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            date TEXT,
            mood TEXT,
            score REAL,
            entry TEXT
        )
    """)

    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()


# Add journal entry
def add_entry(username, mood, score, text):

    conn = sqlite3.connect("journal.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO journal (username, date, mood, score, entry) VALUES (?, ?, ?, ?, ?)",
        (
            username,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            mood,
            score,
            text
        )
    )

    conn.commit()
    conn.close()


# Get entries for a specific user
def get_entries(username):

    conn = sqlite3.connect("journal.db")
    c = conn.cursor()

    c.execute(
        "SELECT * FROM journal WHERE username=? ORDER BY id DESC",
        (username,)
    )

    data = c.fetchall()

    conn.close()
    return data


# Register new user
def register_user(username, password):

    conn = sqlite3.connect("journal.db")
    c = conn.cursor()

    try:
        c.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False


# Login user
def login_user(username, password):

    conn = sqlite3.connect("journal.db")
    c = conn.cursor()

    c.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = c.fetchone()

    conn.close()

    return user