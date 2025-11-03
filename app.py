from fastapi import FastAPI
from datetime import datetime
from models import SongChoice, ClaimedArea, User, GPSPoint

app = FastAPI()

# We're not attaching a db yet, so this just lives in memory while the app runs.  Any restart empties it out
areas = []


@app.get("/")
async def root():
    return {"message": "This is the base address of the API for managing the location data of the app"}

@app.get("/claimedArea/")
async def list_areas():
    return {"areas": areas}

@app.get("/claimedArea/search")
async def find_area(location: GPSPoint):
    # TODO probably the hardest math is taking a current location and finding who it overlaps with
    # should return a ClaimedArea object
    return {"message": "This will be a model object"}

@app.post("/claimedArea/claim")
async def claim_area(area: ClaimedArea):
    # TODO once you have the locations derive the bounds and get info from the authenticated user
    #new_area = ClaimedArea(verts=vertices, user=current_user, song=song)
    areas.append(area)
    return area