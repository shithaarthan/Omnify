"""
Main FastAPI application file defining API endpoints.
"""
import sqlite3 # <-- Make sure this is imported
from fastapi import FastAPI, Depends, HTTPException, Query
from typing import List

from models import BookingRequest, Class, Booking
from db import init_db, get_db
from utils import convert_to_timezone

app = FastAPI(
    title="Omnify Fitness Studio API",
    description="A simple API to book fitness classes.",
    version="1.0.0"
)

# Initialize the database on startup
init_db()

@app.get("/classes", response_model=List[Class], summary="Get a list of available classes")
# ... (This function does not need to change) ...
def list_classes(tz: str = "UTC", db: sqlite3.Connection = Depends(get_db)):
    # ... (no changes here) ...
    cursor = db.cursor()
    cursor.execute("SELECT id, name, date_time, instructor, available_slots FROM classes WHERE available_slots > 0")
    classes_data = cursor.fetchall()
    result = []
    for row in classes_data:
        converted_time = convert_to_timezone(row["date_time"], tz)
        result.append(Class(id=row["id"], name=row["name"], date_time=converted_time, instructor=row["instructor"], available_slots=row["available_slots"]))
    return result

@app.post("/book", status_code=201, summary="Book a spot in a class")
def book_class(request: BookingRequest, db: sqlite3.Connection = Depends(get_db)):
    """
    Books a spot for a client in a specific class.
    This endpoint is now protected against duplicate bookings.
    """
    cursor = db.cursor()
    
    try:
        # Atomically check for slots and decrement
        cursor.execute(
            "UPDATE classes SET available_slots = available_slots - 1 WHERE id = ? AND available_slots > 0",
            (request.class_id,)
        )

        if cursor.rowcount == 0:
            cursor.execute("SELECT available_slots FROM classes WHERE id = ?", (request.class_id,))
            class_exists = cursor.fetchone()
            if not class_exists:
                raise HTTPException(status_code=404, detail=f"Class with id {request.class_id} not found.")
            else:
                raise HTTPException(status_code=400, detail="No available slots for this class.")

        # If the update was successful, create the booking record
        cursor.execute(
            "INSERT INTO bookings (class_id, client_name, client_email) VALUES (?, ?, ?)",
            (request.class_id, request.client_name, request.client_email)
        )
        db.commit()

    except sqlite3.IntegrityError:
        # This error is raised by the UNIQUE constraint in the database
        db.rollback() # Rollback the transaction to be safe
        raise HTTPException(
            status_code=409,  # 409 Conflict is the perfect status code for this
            detail="You have already booked this class."
        )

    return {"message": "Booking successful", "class_id": request.class_id, "client_email": request.client_email}

@app.get("/bookings", response_model=List[Booking], summary="Get bookings for a client")
# ... (This function does not need to change) ...
def get_user_bookings(email: str = Query(..., description="Client's email to fetch bookings for."), db: sqlite3.Connection = Depends(get_db)):
    # ... (no changes here) ...
    cursor = db.cursor()
    cursor.execute("SELECT id, class_id, client_name, client_email FROM bookings WHERE client_email = ?", (email,))
    bookings_data = cursor.fetchall()
    if not bookings_data:
        raise HTTPException(status_code=404, detail=f"No bookings found for email {email}.")
    return [Booking(**row) for row in bookings_data]