from pydantic import BaseModel, EmailStr
from datetime import datetime

class Class(BaseModel):
    id: int
    name: str
    date_time: datetime
    instructor: str
    available_slots: int

class BookingRequest(BaseModel):
    class_id: int
    client_name: str
    client_email: EmailStr

class Booking(BaseModel):
    id: int
    class_id: int
    client_name: str
    client_email: EmailStr
