from fastapi import APIRouter
from schemas.schemas import UserSchema
from models.models import User
from sqlalchemy import text, select, insert, update
from src.sql import sql_engine

router = APIRouter(prefix="/User", tags=["User"])

@router.get("/")
async def get_users(id=None, name=None, is_active=True):
    """
    Returns 1 or many users depending on search criteria, default to only active users
    """
    #session = Session(sql_engine)
    stmt = select(User)
    with sql_engine.connect() as conn:
        users = conn.execute(stmt)

    return [dict(r._mapping) for r in users]

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
    with sql_engine.connect() as conn:
        user = conn.execute(insert(User).values(name=username))
        conn.commit()
    return user