from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..schemas import UserLogin, Token
from ..database import get_db
from ..models import User
from ..utils import verify
from ..oauth2 import create_access_token

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    # Get user's credentials from DB
    user = db.query(User).filter(User.email == user_credentials.username).first()

    # Check if user exists. If not, raise a HTTP exception
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")

    # Check if user supplied password and stored password match. If not, raise a HTTP exception. 
    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # If user exists in DB and passwords match then create an access token
    access_token = create_access_token(data = {"user_id": user.id})

    # Pass the access token to the front-end
    return {"access_token": access_token, "token_type": "bearer"}
