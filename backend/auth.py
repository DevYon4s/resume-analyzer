from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import jwt
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])


#secret key to sign the JWT tokens for now to keep the projects structure as it's described in the test project, i used a hardcoded key but for production,the key should be generated like import secrets SECRET_KEy= secrets.token_urlsafe(32) and stored it in an environment variable file.
SECRET_KEY = "y7Jk9s8Lw3Qp2Zx1Vb6Nf4Tg5Rj0Hc2P"
#HS256 algorithm for signing the JWT tokens
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Fake user for demonstration purposese
FAKE_USER = {
    "username": "admin",
    "password": "password123"
}

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != FAKE_USER["username"] or form_data.password != FAKE_USER["password"]:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": form_data.username, "exp": expire}
    #returns a JWT token with the username as the subject and an expiration time after hardcoded validation of the username and password
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}