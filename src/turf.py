from fastapi import APIRouter
from models.models import Turf
from schemas.schemas import TurfSchema

router = APIRouter(prefix="/Turf", tags=["Turf"])

@router.get("/", response_model=TurfSchema)
async def list_turfs():
    """
    Return a list of all turfs at this point
    """
    # Currently broken, it relies on having "hashable" data types, points and polygons are not
    return Turf

@router.post("/")
async def claim_turf():
    """
    Create a new turf entry, will need a gigantic json file at some point
    """
    # TODO once you have the locations derive the bounds and get info from the authenticated user
    #new_area = Turf(verts=vertices, user=current_user, song=song)
    Turf.create(turf)
