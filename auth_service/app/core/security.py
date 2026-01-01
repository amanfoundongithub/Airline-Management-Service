
# JWT helpers
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

# Security
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Settings
from typing import Dict, Any, Optional
from app.config.settings import settings

from app.schema.token import TokenData
from app.schema.user import UserResponse
from app.schema.object_id import PyObjectId
from app.repository.user import UserRepository, get_user_repository


# ------------------- SECURITY SCHEME (SWAGGER) ---------------------------
bearer_scheme = HTTPBearer(auto_error=False)
# -------------------------------------------------------------------------


# ---------------------- JWT TOKEN HELPERS --------------------------------

def create_jwt_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None,
):
    payload = {"sub": data}

    expire = (
        datetime.now(timezone.utc) + expires_delta
        if expires_delta
        else datetime.now(timezone.utc)
        + timedelta(minutes=settings.security.access_token_expiration_in_minutes)
    )

    payload.update({"exp": expire})

    return jwt.encode(
        payload,
        settings.security.jwt_secret_key,
        algorithm=settings.security.jwt_algorithm,
    )


def decode_jwt_token(token: str) -> Optional[TokenData]:
    try:
        payload = jwt.decode(
            token,
            settings.security.jwt_secret_key,
            algorithms=[settings.security.jwt_algorithm],
        )

        sub = payload.get("sub")
        if sub is None:
            return None

        return TokenData(sub=sub)

    except JWTError:
        return None

# -------------------------------------------------------------------------


# ---------------------- CURRENT USER DEPENDENCY --------------------------

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserResponse:

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    token_data = decode_jwt_token(token)

    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = PyObjectId(token_data.sub)
    current_user = await user_repository.find(id=user_id)

    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist",
        )

    return UserResponse(**current_user.model_dump())

# -------------------------------------------------------------------------