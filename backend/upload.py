from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import httpx
import os

router = APIRouter(tags=["upload"])

SECRET_KEY = "y7Jk9s8Lw3Qp2Zx1Vb6Nf4Tg5Rj0Hc2P"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Function to verify the JWT token before allowing file upload
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), user=Depends(verify_token)):
    # Save file locally
    file_location = f"./uploaded/{file.filename}"
    os.makedirs("./uploaded", exist_ok=True)
    with open(file_location, "wb") as f:
        content = await file.read()
        f.write(content)

    # Call n8n webhook 
    n8n_webhook_url = "http://n8n:5678/webhook-test/resume-upload"


    # Send metadata to n8n
    async with httpx.AsyncClient() as client:
        response = await client.post(n8n_webhook_url, json={
            "file_path": file_location,
            "filename": file.filename
        })

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to notify n8n")

    return {"message": "File uploaded successfully and sent to n8n."}