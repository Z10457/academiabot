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

def add_assignment_row(course, user_id, assignment_name, due_date):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO assignments (course, user_id, assignment_name, due_date) VALUES (?, ?, ?, ?)"
            (course, user_id, assignment_name, due_date),
        )

def list_assignment(course ="", user_id) :
    query = "SELECT course, id , assignment_name, due_date, completed FROM assignments WHERE user_id = ?"
    params = [user_id]
    if course:
        query += " AND LOWER(course) = ?"
        params.append(course.lower())
    query += " ORDER BY user_id"
    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()
    return [
        {"course": r[0], "id": r[1], "assignment_name": r[2], "due_date": r[3], "completed" : bool(r[4])}
        for r in rows
    ]

init_db()