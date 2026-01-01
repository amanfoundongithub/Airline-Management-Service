from typing import Dict, Any
from jose import jwt, JWTError

from src.core.settings import security_settings


def decode_jwt_token(token : str) -> Dict[str, Any] | None:
    try:
        payload = jwt.decode(
            token,
            key = security_settings.JWT_SECRET_KEY,
            algorithms=[security_settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None