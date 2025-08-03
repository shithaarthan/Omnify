"""
Database session management and initialization.
"""
import sqlite3
from config import DATABASE_URL

def get_db():
    """
    FastAPI dependency to get a database connection.
    Yields a connection for the request and ensures it's closed.
    """
    db = sqlite3.connect(DATABASE_URL)
    db.row_factory = sqlite3.Row  # This allows accessing columns by name
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initializes the database schema."""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    # Create classes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            date_time TEXT NOT NULL,
            instructor TEXT NOT NULL,
            available_slots INTEGER NOT NULL CHECK(available_slots >= 0)
        )
    ''')

    # Create bookings table with the new uniqueness constraint
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_id INTEGER NOT NULL,
            client_name TEXT NOT NULL,
            client_email TEXT NOT NULL,
            FOREIGN KEY(class_id) REFERENCES classes(id),
            UNIQUE(class_id, client_email)
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized.")