
# Password helper 
import bcrypt

# JWT helpers
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

# Security
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# Settings 
from typing import Dict, Any, Optional
from config.settings import settings

from schema.token import TokenData
from schema.user import UserResponse
from schema.object_id import PyObjectId
from repository.user import UserRepository, get_user_repository


# ------------------- USER AUTHENTICATION HELPERS -------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "/api/v1/users/login")

# ------------------- PASSWORD ENCRYPTION HANDLERS ------------------------

def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds = settings.security.password_hash_rounds)
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    candidate_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(candidate_bytes, hashed_bytes)

# -------------------------------------------------------------------------


# ---------------------- JWT TOKEN HELPERS --------------------------------

def create_jwt_token(data : Dict[str, Any], expires_delta : Optional[timedelta] = None):

    payload = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else: 
        expire = datetime.now(timezone.utc) + timedelta(minutes = settings.security.access_token_expiration_in_minutes)
    
    payload.update({
        "exp" : expire 
    })

    return jwt.encode(
        payload,
        settings.security.jwt_secret_key,
        algorithm = settings.security.jwt_algorithm
    )

def decode_jwt_token(token : str) -> Optional[TokenData]:
    try:
        payload = jwt.decode(
            token,
            settings.security.jwt_secret_key,
            algorithms = [settings.security.jwt_algorithm]
        )

        sub : str = payload.get("sub")
        if sub is None: 
            return None
        
        return TokenData(
            sub = sub
        )
    
    except JWTError as e:
        return None
    
async def get_current_user(
        token : str = Depends(oauth2_scheme),
        user_repository : UserRepository = Depends(get_user_repository)
) -> UserResponse:
    token_data = decode_jwt_token(token)
    if token_data is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Could not validate bearer token",
            headers = {
                "WWW-Authenticate": "Bearer"
            }
        )
    
    user_id = PyObjectId(token_data.sub)
    current_user = await user_repository.find(id = user_id)
    if current_user is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User does not exist" 
        )
    return UserResponse(**current_user.model_dump()) 

    
# -------------------------------------------------------------------------