# test_api.py
import requests
import json

# The base URL of your running FastAPI application
BASE_URL = "http://127.0.0.1:8000"

def print_response(response):
    """Helper function to print the response in a readable format."""
    print(f"Status Code: {response.status_code}")
    try:
        # Pretty-print the JSON response
        print(json.dumps(response.json(), indent=2))
    except json.JSONDecodeError:
        # If the response is not JSON, print the raw text
        print(f"Response Body: {response.text}")

def test_get_classes():
    """Tests the GET /classes endpoint."""
    print("--- 1. Testing GET /classes (in New York timezone) ---")
    url = f"{BASE_URL}/classes"
    params = {"tz": "America/New_York"}
    
    try:
        response = requests.get(url, params=params)
        print_response(response)
        if response.status_code == 200:
            print("\nSUCCESS: Successfully retrieved the list of classes.")
        else:
            print("\nFAILURE: Could not retrieve classes.")
    except requests.exceptions.ConnectionError as e:
        print(f"\nFAILURE: Could not connect to the API. Is the server running?\nError: {e}")
        return False
    return True

def test_successful_booking():
    """Tests a successful booking via POST /book."""
    print("\n--- 2. Testing a SUCCESSFUL booking (POST /book) ---")
    url = f"{BASE_URL}/book"
    
    # Data for a new booking for a class that should have slots
    payload = {
        "class_id": 1,
        "client_name": "Jane Doe",
        "client_email": "jane.doe@example.com"
    }
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print_response(response)
    
    if response.status_code == 201:
        print("\nSUCCESS: Booking was created successfully.")
        return payload["client_email"] # Return email for the next test
    else:
        print(f"\nFAILURE: Expected status 201, but got {response.status_code}.")
        return None

def verify_booking(client_email):
    """Tests GET /bookings to verify a previous booking."""
    if not client_email:
        print("\nSkipping verification because previous booking failed.")
        return
        
    print(f"\n--- 3. Verifying the booking (GET /bookings?email={client_email}) ---")
    url = f"{BASE_URL}/bookings"
    params = {"email": client_email}
    
    response = requests.get(url, params=params)
    print_response(response)
    
    if response.status_code == 200 and len(response.json()) > 0:
         print(f"\nSUCCESS: Found booking(s) for {client_email}.")
    else:
         print(f"\nFAILURE: Could not find booking for {client_email}.")

def test_booking_full_class():
    """Tests booking a class that has no available slots."""
    print("\n--- 4. Testing booking a FULL class (Expecting Failure) ---")
    url = f"{BASE_URL}/book"
    
    # Class 4 is seeded with 0 slots
    payload = {
        "class_id": 4,
        "client_name": "John Smith",
        "client_email": "john.smith@example.com"
    }
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print_response(response)
    
    if response.status_code == 400:
        print("\nSUCCESS: API correctly blocked booking of a full class.")
    else:
        print(f"\nFAILURE: Expected status 400, but got {response.status_code}.")
        
def test_booking_non_existent_class():
    """Tests booking a class that does not exist."""
    print("\n--- 5. Testing booking a NON-EXISTENT class (Expecting Failure) ---")
    url = f"{BASE_URL}/book"
    
    payload = {
        "class_id": 999, # This class ID should not exist
        "client_name": "Ghost User",
        "client_email": "ghost@example.com"
    }
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print_response(response)
    
    if response.status_code == 404:
        print("\nSUCCESS: API correctly returned 'Not Found' for a non-existent class.")
    else:
        print(f"\nFAILURE: Expected status 404, but got {response.status_code}.")

def test_duplicate_booking():
    """Tests that booking the same class twice with the same email fails."""
    print("\n--- 6. Testing a DUPLICATE booking (Expecting Failure) ---")
    url = f"{BASE_URL}/book"
    
    # This payload is for a class that should have slots
    payload = {
        "class_id": 2,
        "client_name": "Duplicate Tester",
        "client_email": "duplicate@example.com"
    }
    headers = {"Content-Type": "application/json"}
    
    # First booking should succeed
    print("Attempting first booking (should succeed)...")
    response1 = requests.post(url, headers=headers, data=json.dumps(payload))
    if response1.status_code != 201:
        print("FAILURE: The first booking failed, cannot test for duplicates.")
        print_response(response1)
        return

    # Second booking should fail
    print("Attempting second booking (should fail with 409)...")
    response2 = requests.post(url, headers=headers, data=json.dumps(payload))
    print_response(response2)

    if response2.status_code == 409:
        print("\nSUCCESS: API correctly blocked a duplicate booking with a 409 Conflict status.")
    else:
        print(f"\nFAILURE: Expected status 409, but got {response2.status_code}.")

# --- Main execution block ---
if __name__ == "__main__":
    print("=======================================")
    print("  STARTING API ENDPOINT TEST SCRIPT  ")
    print("=======================================")
    
    # Before starting, make sure the API is running and the database is fresh
    print("\nReminder: Make sure you have run `python seed_data.py` before this test.")
    
    # Run tests in sequence
    if test_get_classes():
        email_to_verify = test_successful_booking()
        verify_booking(email_to_verify)
        test_booking_full_class()
        test_booking_non_existent_class()
        test_duplicate_booking()
        
    print("\n=======================================")
    print("           TEST SCRIPT FINISHED          ")
    print("=======================================")