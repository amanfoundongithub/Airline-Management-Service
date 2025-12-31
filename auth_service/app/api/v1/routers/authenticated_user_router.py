from fastapi        import APIRouter, Depends, HTTPException, status

from app.schema.user    import UserCreate, UserLogin, UserResponse
from app.schema.token   import Token
from app.service.user   import UserService, get_user_service

from app.core.exception import UserAlreadyExistsException, UserAuthenticationException
from app.core.security  import create_jwt_token, get_current_user


router = APIRouter(
    prefix = "/users",
    tags = ["Authenticated"],
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
        current_user: UserResponse = Depends(get_current_user),
) -> UserResponse:
    return current_user