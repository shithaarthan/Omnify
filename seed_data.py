# seed_data.py
import sqlite3
from datetime import datetime, timedelta
from config import DEFAULT_TIMEZONE, DATABASE_URL

def seed():
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    # Clear existing data to ensure a clean slate
    cursor.execute("DELETE FROM bookings")
    cursor.execute("DELETE FROM classes")

    # Note: We store naive datetime strings. The application logic assumes they are in DEFAULT_TIMEZONE.
    classes = [
        (1, "Yoga", datetime.now(DEFAULT_TIMEZONE).isoformat(), "Alice", 10),
        (2, "Zumba", (datetime.now(DEFAULT_TIMEZONE) + timedelta(days=1)).isoformat(), "Bob", 5),
        (3, "HIIT", (datetime.now(DEFAULT_TIMEZONE) + timedelta(days=2)).isoformat(), "Charlie", 1),
        (4, "Spin", (datetime.now(DEFAULT_TIMEZONE) + timedelta(days=3)).isoformat(), "David", 0), # A full class
    ]

    cursor.executemany("INSERT INTO classes (id, name, date_time, instructor, available_slots) VALUES (?, ?, ?, ?, ?)", classes)
    conn.commit()
    conn.close()
    print("Database seeded with sample data.")

if __name__ == "__main__":
    # Ensure the DB schema exists before seeding
    from db import init_db
    init_db()
    seed()