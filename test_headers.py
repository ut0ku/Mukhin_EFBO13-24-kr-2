import requests
import json

BASE_URL = "http://127.0.0.1:8001/headers"

def test_headers():
    print("=== Testing /headers endpoint ===")
    
    print("\n1. Успешный запрос (с правильными заголовками)...")
    headers_valid = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,es;q=0.8"
    }
    r = requests.get(BASE_URL, headers=headers_valid)
    print(f"Status: {r.status_code}")
    print(f"Response: {json.dumps(r.json(), indent=4)}")
    
    print("\n2. Отсутствует User-Agent...")
    headers_no_agent = {
        "Accept-Language": "ru-RU,ru;q=0.9"
    }
    headers_no_agent["User-Agent"] = None
    
    req = requests.Request('GET', BASE_URL, headers={"Accept-Language": "ru-RU,ru;q=0.9"})
    prep = req.prepare()
    if 'User-Agent' in prep.headers:
        del prep.headers['User-Agent']
    
    s = requests.Session()
    r = s.send(prep)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.json()}")

    print("\n3. Отсутствует Accept-Language...")
    headers_no_lang = {
        "User-Agent": "Mozilla/5.0"
    }
    r = requests.get(BASE_URL, headers=headers_no_lang)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.json()}")

    print("\n4. Неправильный формат Accept-Language...")
    headers_invalid_lang = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "invalid_format_123_!!!"
    }
    r = requests.get(BASE_URL, headers=headers_invalid_lang)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.json()}")

if __name__ == "__main__":
    test_headers()
