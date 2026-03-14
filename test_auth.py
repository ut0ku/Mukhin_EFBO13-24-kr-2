import requests
import json

BASE_URL = "http://127.0.0.1:8001"

def test_auth():
    print("=== Testing Authentication Endpoint ===")
    
    session = requests.Session()
    
    print("\n1. Вход в систему (POST /login) с правильными данными...")
    login_data = {"username": "user123", "password": "password123"}
    r_login = session.post(f"{BASE_URL}/login", json=login_data)
    print(f"Status Code: {r_login.status_code}")
    print(f"Response: {r_login.json()}")
    
    # Проверка, что cookie сохранены
    cookies = session.cookies.get_dict()
    print(f"Cookies: {cookies}")
    
    print("\n2. Запрос профиля (GET /user) с валидным cookie...")
    r_user = session.get(f"{BASE_URL}/user")
    print(f"Status Code: {r_user.status_code}")
    print(f"Response: {json.dumps(r_user.json(), indent=4)}")
    
    print("\n3. Запрос профиля (GET /user) БЕЗ cookie...")
    r_no_cookie = requests.get(f"{BASE_URL}/user")
    print(f"Status Code: {r_no_cookie.status_code}")
    print(f"Response: {r_no_cookie.json()}")
    
    print("\n4. Запрос профиля (GET /user) с НЕДЕЙСТВИТЕЛЬНЫМ cookie...")
    invalid_cookies = {"session_token": "invalid_token_12345"}
    r_invalid_cookie = requests.get(f"{BASE_URL}/user", cookies=invalid_cookies)
    print(f"Status Code: {r_invalid_cookie.status_code}")
    print(f"Response: {r_invalid_cookie.json()}")

if __name__ == "__main__":
    test_auth()
