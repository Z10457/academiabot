import sqlite3

DB_FILE = "user.db"

def get_connection():
    return sqlite3.connect(DB_FILE)

def init_db():
    with get_connection() as conn : 
        conn.execute(
            "CREATE IF NOT EXISTS assignments(" 
            "id INTEGER PRIMARY KEY, "
            "user_id TEXT NOT NULL, "
            "course TEXT, assignment_name TEXT , due_date TEXT, "
            "completed INTEGER DEFAULT 0)"
        )

def assignment_exists (course, user_id, assignment_name, due_date):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT 1 FROM assignments WHERE course = ? AND user_id = ? AND assignment_name = ? AND due_date = ?",
            (course, user_id, assignment_name, due_date), #this is the tuple which it selects from, the question marks abobve.
        ).fetchone()
    return row is not None
        