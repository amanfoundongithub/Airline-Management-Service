from fastapi        import APIRouter, Depends, HTTPException, status
from typing import Any, Dict

from app.schema.object_id import PyObjectId
from app.schema.user import UserCreate, UserLogin, UserResponse, UserUpdate, UserPasswordUpdate, UserUpdateStatus
from app.schema.token   import Token, TokenData
from app.service.user   import UserService, get_user_service

from app.core.exception import UserAlreadyExistsException, UserAuthenticationException
from app.core.security  import create_jwt_token, get_current_user


router = APIRouter(
    prefix = "/users",
    tags = ["User Self-Service"],
    deprecated = False,
    include_in_schema = True
)

@router.get(
    "/me",
    summary =
    """
    Details obtained from authentication token
    """,
    description =
    """
    Details obtained from authentication token
    """
)
async def get_current_active_user(
        current_user: TokenData = Depends(get_current_user),
) -> TokenData:
    return current_user



@router.patch(
    "/me",
    summary =
    """
    Update user's profile
    """,
    description =
    """
    Update user's profile
    """
)
async def update_current_active_user(
    details: UserUpdate,
    current_user: TokenData = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
) -> UserResponse:
    user_id = PyObjectId(current_user.sub["id"])
    return await user_service.update(user_id, details)



@router.patch(
    "/me/password",
    summary =
    """
    Allows to update password
    """,
    description =
    """
    Update the password of an existing user
    """
)
async def update_password_current_user(
        request : UserPasswordUpdate,
        current_user: TokenData = Depends(get_current_user),
        user_service: UserService = Depends(get_user_service)
) -> UserUpdateStatus:
    email = current_user.sub["email"]
    await user_service.update_password(str(email), request.old_password, request.new_password)
    return UserUpdateStatus()

