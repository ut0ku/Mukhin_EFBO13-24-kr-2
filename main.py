from fastapi import FastAPI, HTTPException, Query, Response, Cookie, Header, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List, Annotated
import uuid
import time
from datetime import datetime
import re
from itsdangerous import Signer, BadSignature

app = FastAPI()

# Секретный ключ для подписи cookie
SECRET_KEY = "my_super_secret_key_for_testing"
signer = Signer(SECRET_KEY)


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = Field(None, gt=0)
    is_subscribed: Optional[bool] = False

@app.post("/create_user")
async def create_user(user: UserCreate):
    return user

sample_product_1 = {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
}
sample_product_2 = {
    "product_id": 456,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99
}
sample_product_3 = {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99
}
sample_product_4 = {
    "product_id": 101,
    "name": "Headphones",
    "category": "Accessories",
    "price": 99.99
}
sample_product_5 = {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99
}

sample_products = [
    sample_product_1, sample_product_2, sample_product_3, 
    sample_product_4, sample_product_5
]

@app.get("/products/search")
async def search_products(
    keyword: str, 
    category: Optional[str] = None, 
    limit: int = 10
):
    results = []
    for product in sample_products:
        if keyword.lower() in product["name"].lower():
            if category is None or product["category"].lower() == category.lower():
                results.append(product)
                
    return results[:limit]

@app.get("/product/{product_id}")
async def get_product(product_id: int):
    for product in sample_products:
        if product["product_id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

sessions = {}

# Хранилище пользователей
users_db = {
    "user123": {
        "password": "password123",
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "profile": {
            "name": "User 123",
            "email": "user123@example.com",
            "role": "admin"
        }
    }
}

class LoginData(BaseModel):
    username: str
    password: str

@app.post("/login")
async def login(response: Response, login_data: LoginData):
    user = users_db.get(login_data.username)
    if not user or user["password"] != login_data.password:
        response.status_code = 401
        return {"message": "Unauthorized"}
    
    # Генерация токена: user_id.timestamp.signature
    timestamp = int(time.time())
    payload = f"{user['id']}.{timestamp}"
    
    signed_token_bytes = signer.sign(payload.encode("utf-8"))
    signed_token = signed_token_bytes.decode("utf-8")
    
    sessions[signed_token] = login_data.username
    
    response.set_cookie(
        key="session_token", 
        value=signed_token, 
        httponly=True,
        secure=False,
        max_age=300
    )
    
    return {"message": "Login successful"}

@app.get("/user")
async def get_user(session_token: Optional[str] = Cookie(None)):
    if not session_token:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})
    
    if session_token in sessions:
        username = sessions[session_token]
        return users_db[username]["profile"]
    
    return JSONResponse(status_code=401, content={"message": "Unauthorized"})

@app.get("/profile")
async def get_profile(response: Response, session_token: Optional[str] = Cookie(None)):
    if not session_token:
        response.status_code = 401
        return {"message": "Invalid session"}

    try:
        payload_bytes = signer.unsign(session_token.encode("utf-8"))
        payload = payload_bytes.decode("utf-8")
    except BadSignature:
        response.status_code = 401
        return {"message": "Invalid session"}
        
    try:
        user_id, timestamp_str = payload.rsplit('.', 1)
        timestamp = int(timestamp_str)
    except (ValueError, TypeError):
        response.status_code = 401
        return {"message": "Invalid session"}
        
    current_time = int(time.time())
    elapsed = current_time - timestamp
    
    # 1. Если прошло больше 5 минут (300 сек) -> Сессия истекла
    if elapsed > 300:
        response.status_code = 401
        return {"message": "Session expired"}
    
    user_profile = None
    for user_info in users_db.values():
        if user_info["id"] == user_id:
            user_profile = user_info["profile"]
            break
            
    if not user_profile:
        response.status_code = 401
        return {"message": "Invalid session"}
        
    # 2. Обновление токена, если прошло от 3 до 5 минут
    if 180 <= elapsed <= 300:
        new_timestamp = int(time.time())
        new_payload = f"{user_id}.{new_timestamp}"
        new_signed_token_bytes = signer.sign(new_payload.encode("utf-8"))
        new_signed_token = new_signed_token_bytes.decode("utf-8")
        
        response.set_cookie(
            key="session_token",
            value=new_signed_token,
            httponly=True,
            secure=False,
            max_age=300
        )
        
    return user_profile

strict_pattern = re.compile(r"^en-US,en;q=0\.9,es;q=0\.8$")

class CommonHeaders(BaseModel):
    user_agent: str = Field(...)
    accept_language: str = Field(...)

    @field_validator("accept_language")
    def validate_accept_language(cls, v):
        if not strict_pattern.match(v):
            raise ValueError("Accept-Language header format is invalid")
        return v

# Зависимость для извлечения и валидации заголовков
async def get_common_headers(
    user_agent: Optional[str] = Header(None, alias="User-Agent"),
    accept_language: Optional[str] = Header(None, alias="Accept-Language")
) -> CommonHeaders:
    if not user_agent or str(user_agent).strip() == "":
        raise HTTPException(status_code=400, detail="User-Agent header is missing")
    if not accept_language or str(accept_language).strip() == "":
        raise HTTPException(status_code=400, detail="Accept-Language header is missing")
        
    try:
        return CommonHeaders(user_agent=user_agent, accept_language=accept_language)
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Accept-Language header format is invalid")

@app.get("/headers")
async def get_headers_route(headers: CommonHeaders = Depends(get_common_headers)):
    return {
        "User-Agent": headers.user_agent,
        "Accept-Language": headers.accept_language
    }

@app.get("/info")
async def get_info_route(response: Response, headers: CommonHeaders = Depends(get_common_headers)):
    # Установка кастомного заголовка ответа с текущим временем
    current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    response.headers["X-Server-Time"] = current_time
    
    return {
        "message": "Добро пожаловать! Ваши заголовки успешно обработаны.",
        "headers": {
            "User-Agent": headers.user_agent,
            "Accept-Language": headers.accept_language
        }
    }




