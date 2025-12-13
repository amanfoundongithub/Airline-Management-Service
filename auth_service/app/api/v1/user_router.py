from fastapi        import APIRouter, Depends, HTTPException, status

from schema.user    import UserCreate, UserLogin, UserResponse
from service.user   import UserService, get_user_service
from core.exception import UserAlreadyExistsException, UserAuthorizationException


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
    response_model = UserResponse,
    status_code = status.HTTP_200_OK,
    summary = "Authenticates a user account"
)
async def login_route(
    credentials : UserLogin,
    user_service: UserService = Depends(get_user_service)
):
    try:
        return await user_service.authenticate(credentials) 
    
    except UserAuthorizationException as e:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail = str(e))
    

    
