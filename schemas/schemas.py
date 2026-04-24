from datetime import datetime
from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    name: str
    joined: datetime
    is_active: bool

# Need to update this too
class TurfSchema(BaseModel):
    id: int
    user_id: int
    upload_date: datetime
    polygon: str
    centroid_lat: float
    centroid_long: float
    area_sqkm: float
    area_avg_radius: float
    last_boosted: datetime
    protected: bool