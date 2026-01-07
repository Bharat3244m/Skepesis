import requests
import sys
import json

# Configuration
BASE_URL = "http://127.0.0.1:8080"
TEST_USER = {
    "username": "teststudent",
    "email": "test@example.com",
    "password": "password123"
}

def print_step(message):
    print(f"\n🔹 {message}")

def print_success(message):
    print(f"✅ {message}")

def print_error(message, response=None):
    print(f"❌ {message}")
    if response:
        print(f"   Status: {response.status_code}")
        try:
            print(f"   Detail: {response.json()}")
        except:
            print(f"   Raw: {response.text}")
    sys.exit(1)

def check_health():
    print_step("Checking API Health...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print_success("API is Online")
            print(f"   Response: {response.json()}")
        else:
            print_error("API Health Check Failed", response)
    except requests.exceptions.ConnectionError:
        print_error("Could not connect to server. Is it running? (http://127.0.0.1:8000)")

def register_user():
    print_step(f"Registering User: {TEST_USER['email']}...")
    payload = {
        "username": TEST_USER["username"],
        "email": TEST_USER["email"],
        "password": TEST_USER["password"]
    }
    response = requests.post(f"{BASE_URL}/api/auth/register", json=payload)
    
    if response.status_code == 200:
        print_success("Registration Successful")
        return True
    elif response.status_code == 400 and "already registered" in response.text:
        print("   ℹ️  User already exists (Skipping registration)")
        return True
    else:
        print_error("Registration Failed", response)

def login_user():
    print_step("Logging In...")
    # NOTE: OAuth2 expects form-data with 'username' and 'password' fields
    # We map email -> username field as per FastAPI convention
    payload = {
        "username": TEST_USER["email"], 
        "password": TEST_USER["password"]
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/login", data=payload)
    
    if response.status_code == 200:
        data = response.json()
        token = data.get("access_token")
        if token:
            print_success("Login Successful. Token received.")
            return token
        else:
            print_error("Login successful but no token returned", response)
    else:
        print_error("Login Failed", response)

def test_protected_route(token):
    print_step("Testing Protected Route (/api/auth/me)...")
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
    
    if response.status_code == 200:
        user = response.json()
        print_success(f"Verified Identity: {user['email']} (Role: {user['role']})")
    else:
        print_error("Protected Route Access Failed", response)

if __name__ == "__main__":
    print("🚀 Starting Backend API Test...")
    
    # 1. Health Check
    check_health()
    
    # 2. Register
    register_user()
    
    # 3. Login
    access_token = login_user()
    
    # 4. Access Protected Data
    test_protected_route(access_token)
    
    print("\n✨ All systems go! The Backend is working perfectly.")