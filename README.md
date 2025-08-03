# 🧪 Fitness Class Booking API

This is a simple booking API for a fictional fitness studio, built with Python and FastAPI.

## 🧑‍💻 Developer's Note

Beyond the core requirements of this assignment, I wanted to highlight an additional feature implemented and share a bit about my other work.

**Proactive Feature Enhancement:**
I noticed that the base requirements would allow a user to book the same class multiple times. To address this, I implemented a `UNIQUE` constraint at the database level and corresponding API error handling (`HTTP 409 Conflict`) to prevent this. This reflects a real-world business rule and adds a layer of robustness to the API.

**Agentic Developer Profile:**
My passion lies in creating intelligent, autonomous systems. As an Agentic Developer, I build applications that can reason, plan, and act on behalf of a user to accomplish complex goals.

A prime example of this is my Telegram bot, **EquiSage**.
*   **Bot Username:** `@EquiSage_bot`
*   **Functionality:** This agentic bot retrieves and synthesizes real-time financial data from multiple sources. It performs analysis on market trends and can generate a consolidated PDF report on demand, delivering complex insights through a simple chat interface.

Thank you for the opportunity and for reviewing my work.


## ✨ Features

- View available classes with correct timezone conversion.
- Book a spot in a class with atomic updates to prevent overbooking.
- View all bookings for a specific client.
- Modular, well-documented, and tested code.
- Centralized configuration and database management.

## ⚙️ Setup and Run

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourname/fitness-booking-api.git
    cd fitness-booking-api
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Initialize and seed the database:**
    This script will create `fitness.db` and populate it with sample classes.
    ```bash
    python seed_data.py
    ```

4.  **Run the application:**
    ```bash
    uvicorn main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`.

## 📚 API Documentation

Once the server is running, interactive API documentation (provided by Swagger UI) is available at:

**http://127.0.0.1:8000/docs**

