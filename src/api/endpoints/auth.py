from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from src.core.config import get_settings

settings = get_settings()
security = HTTPBasic()

router = APIRouter()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = settings.SWAGGER_USERNAME
    correct_password = settings.SWAGGER_PASSWORD
    
    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username 