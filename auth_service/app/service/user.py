from app.repository.user import get_user_repository, UserRepository
from app.schema.user     import UserResponse, UserCreate, UserLogin, UserInDB

from app.core.security   import hash_password, verify_password
from app.core.exception import UserAlreadyExistsException, UserAuthenticationException
from typing          import Optional

class UserService:

    def __init__(self, user_repo : UserRepository = None):
        self.repository = user_repo or get_user_repository()
    
    async def create(self, request : UserCreate) -> Optional[UserResponse]:
        is_existing_user = await self.repository.find(email = str(request.email))
        if is_existing_user:
            raise UserAlreadyExistsException(f"User already exists with the email:{request.email}")

        hashed_password = hash_password(request.password)
        user_in_db = UserInDB(
            **request.model_dump(exclude = {
                "password"
            }),
            hashed_password = hashed_password
        )
        created_user_in_db = await self.repository.insert(user_in_db)
        return UserResponse(
            **created_user_in_db.model_dump()
        )

    async def authenticate(self, credentials : UserLogin) -> Optional[UserResponse]:
        user_in_db = await self.repository.find(email = str(credentials.email))
        if not user_in_db:
            raise UserAuthenticationException(f"User with email:{credentials.email} does not exist.")
        
        correct = verify_password(credentials.password, user_in_db.hashed_password)
        if not correct:
            raise UserAuthenticationException(f"Incorrect password for user with email:{credentials.email}")
    
        return UserResponse(
            **user_in_db.model_dump()
        )

def get_user_service() -> UserService:
    return UserService() 