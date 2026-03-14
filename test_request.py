import requests
import json

def test_create_user():
    url = "http://127.0.0.1:8000/create_user"
    payload = {
        "name": "Alice",
        "email": "alice@example.com",
        "age": 30,
        "is_subscribed": True
    }
    
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {json.dumps(response.json(), indent=4)}")

if __name__ == "__main__":
    import time
    time.sleep(2)
    try:
        test_create_user()
    except Exception as e:
        print(f"Error: {e}")
