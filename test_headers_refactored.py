import requests
import json

BASE_URL = "http://127.0.0.1:8001"

def test_headers_refactored():
    headers_valid = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0)",
        "Accept-Language": "en-US,en;q=0.9"
    }

    print("=== Testing GET /headers ===")
    r_headers = requests.get(f"{BASE_URL}/headers", headers=headers_valid)
    print(f"Status: {r_headers.status_code}")
    print(f"Response: {json.dumps(r_headers.json(), indent=4)}")
    
    print("\n=== Testing GET /info ===")
    r_info = requests.get(f"{BASE_URL}/info", headers=headers_valid)
    print(f"Status: {r_info.status_code}")
    print(f"Response JSON: {json.dumps(r_info.json(), indent=4)}")
    print(f"Response Headers X-Server-Time: {r_info.headers.get('X-Server-Time')}")

    print("\n=== Testing Errors ===")
    r_err = requests.get(f"{BASE_URL}/info", headers={"User-Agent": "Moz"})
    print(f"Status (missing Accept-Language): {r_err.status_code}")
    
    r_err_format = requests.get(f"{BASE_URL}/info", headers={"User-Agent": "Moz", "Accept-Language": "invalid!!!@#$%^"})
    print(f"Status (invalid formst Accept-Language): {r_err_format.status_code}")
    print(f"Response: {r_err_format.json()}")


if __name__ == "__main__":
    test_headers_refactored()
