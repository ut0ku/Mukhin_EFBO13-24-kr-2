import requests
import json

BASE_URL = "http://127.0.0.1:8001"

def test_signed_auth():
    print("=== Testing Signed Authentication Endpoint ===")
    
    session = requests.Session()
    
    print("\n1. Вход в систему (POST /login)...")
    login_data = {"username": "user123", "password": "password123"}
    r_login = session.post(f"{BASE_URL}/login", json=login_data)
    print(f"Status Code: {r_login.status_code}")
    print(f"Response: {r_login.json()}")
    
    cookies = session.cookies.get_dict()
    print(f"Cookies: {cookies}")
    session_token = cookies.get('session_token')
    print(f"Обратите внимание на формат токена (user_id.signature): {session_token}")
    
    print("\n2. Запрос профиля (GET /profile) с правильным подписанным cookie...")
    r_profile = session.get(f"{BASE_URL}/profile")
    print(f"Status Code: {r_profile.status_code}")
    print(f"Response: {json.dumps(r_profile.json(), indent=4)}")
    
    print("\n3. Запрос профиля (GET /profile) с измененным (поддельным) cookie...")
    fake_token = session_token[:-1] + ('a' if session_token[-1] != 'a' else 'b')
    r_fake = requests.get(f"{BASE_URL}/profile", cookies={"session_token": fake_token})
    print(f"Status Code: {r_fake.status_code}")
    print(f"Response: {r_fake.json()}")

    print("\n4. Запрос профиля (GET /profile) с токеном без подписи (только UUID)...")
    uuid_only = session_token.split('.')[0]
    r_uuid = requests.get(f"{BASE_URL}/profile", cookies={"session_token": uuid_only})
    print(f"Status Code: {r_uuid.status_code}")
    print(f"Response: {r_uuid.json()}")

if __name__ == "__main__":
    test_signed_auth()
