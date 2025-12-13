
# Password helper 
import bcrypt

# JWT helpers
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

# Settings 
from typing import Dict, Any, Optional
from config.settings import settings




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

def decode_jwt_token(token : str) -> Optional[Dict[str, Any]]:
    try:
        return jwt.decode(
            token,
            settings.security.jwt_secret_key,
            algorithms = [settings.security.jwt_algorithm]
        )
    
    except JWTError as e:
        return None

# -------------------------------------------------------------------------