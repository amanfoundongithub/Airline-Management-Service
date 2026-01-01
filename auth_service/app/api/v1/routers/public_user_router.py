from fastapi        import APIRouter, Depends, HTTPException, status

from app.core.rbac import get_user_permissions
from app.schema.user    import UserCreate, UserLogin, UserResponse
from app.schema.token   import Token
from app.service.user   import UserService, get_user_service

from app.core.exception import UserAlreadyExistsException, UserAuthenticationException
from app.core.security  import create_jwt_token


router = APIRouter(
    prefix = "/auth",
    tags = ["Public Authorization"],
    deprecated = False,
    include_in_schema = True
)

@router.post(
    "/register",
    summary =
    """
    Create a new user account
    """,
    description =
    """
    Create a new user account
    """
)
async def register_route(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
) -> UserResponse:
    try:
        return await user_service.create(user_data)
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,
                            detail = {
                                "message" : str(e)
                            })

@router.post(
    "/login",
    summary =
    """
    Authenticates a user, returning secure JWT token
    """,
    description =
    """
    Authenticates a user, returning secure JWT token
    """
)
async def login_route(
    credentials : UserLogin,
    user_service: UserService = Depends(get_user_service)
) -> Token:
    try:
        data = await user_service.authenticate(credentials)
        permissions = list(get_user_permissions(data.role))
        sub = {
            "permissions" : permissions,
            "role" : data.role,
            "name" : data.name
        }

        return Token(
            access_token = create_jwt_token(
                data = sub
            )
        )
    
    except UserAuthenticationException as e:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail = str(e))