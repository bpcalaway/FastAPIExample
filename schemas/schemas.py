from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    name: str
    is_active: bool

# Need to update this too
class TurfSchema(BaseModel):
    id: int
    user_id: int