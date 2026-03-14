import requests
import json

def test_endpoints():
    print("Testing /product/{product_id}")
    url_get = "http://127.0.0.1:8001/product/123"
    r_get = requests.get(url_get)
    print(f"Status: {r_get.status_code}")
    print(json.dumps(r_get.json(), indent=4))
    
    print("\nTesting /products/search")
    url_search = "http://127.0.0.1:8001/products/search?keyword=phone&category=Electronics&limit=5"
    r_search = requests.get(url_search)
    print(f"Status: {r_search.status_code}")
    print(json.dumps(r_search.json(), indent=4))

if __name__ == "__main__":
    test_endpoints()