from fastapi        import APIRouter, Depends, HTTPException, status

from app.schema.user    import UserCreate, UserLogin, UserResponse
from app.schema.token   import Token
from app.service.user   import UserService, get_user_service

from app.core.exception import UserAlreadyExistsException, UserAuthenticationException
from app.core.security  import create_jwt_token, get_current_user


router = APIRouter(
    prefix = "/users",
    tags = ["users"]
)

@router.post(
    "/register",
    response_model = UserResponse,
    status_code = status.HTTP_201_CREATED,
    summary = "Creates a new user account"
)
async def register_route(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    try:
        return await user_service.create(user_data)
    
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT,
                            detail = str(e)) 

@router.post(
    "/login",
    response_model = Token,
    status_code = status.HTTP_200_OK,
    summary = "Authenticates a user account, returning a JWT"
)
async def login_route(
    credentials : UserLogin,
    user_service: UserService = Depends(get_user_service)
):
    try:
        data = await user_service.authenticate(credentials) 
        sub = str(data.id)

        return Token(
            access_token = create_jwt_token(
                data = sub
            )
        )
    
    except UserAuthenticationException as e:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail = str(e))
    

@router.get(
    "/me",
    response_model = UserResponse,
    status_code = status.HTTP_200_OK,
    summary = "Test route to get user details"
)
async def get_me_route(
    current_user : UserResponse = Depends(get_current_user)
):
    return current_user