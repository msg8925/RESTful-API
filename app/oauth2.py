from fastapi import HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from .schemas import TokenData
from .database import get_db
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .models import User
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# Get hashing data from environment variables
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# Create a JWT access token
def create_access_token(data: dict):
    
    # Create a copy of dict 'data' and store it in 'to_encode'
    to_encode = data.copy()

    # Create an expiration datetime
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Append the expiration datetime to the dict 'to_encode'
    to_encode.update({"exp": expire})

    # Create the JWT token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # Return the JWT token
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:
        # De-hash the token using the SECRET_KEY
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        # Extract the 'user_id' from the token
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)

    except JWTError:
        raise credentials_exception

    return token_data


# Validates whether a user is currently logged in
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    
    # Store the HTTP exception in 'credentials_exception'
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    # Perform token verification check           
    token = verify_access_token(token, credentials_exception)

    # Get user from DB using 'user_id' which is stored in token
    user = db.query(User).filter(User.id == token.id).first()

    return user 