from fastapi import APIRouter
from schemas.schemas import UserSchema
from models.models import User

router = APIRouter(prefix="/User", tags=["User"])

@router.get("/", response_model=UserSchema)
async def get_users(id=None, name=None, is_active=True):
    """
    Returns 1 or many users depending on search criteria, default to only active users
    """
    #session = Session(sql_engine)

    return User

@router.patch("/")
async def patch_user(user: UserSchema):
    """
    Update User info, used for deactivating accounts or changing usernames.
    """
    return User
    

@router.post("/")
async def post_user(username: str):
    """
    Should only be used for creating a new user, fail if name is already taken with message
    """
    User.create(name=username)