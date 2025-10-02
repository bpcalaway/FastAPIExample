from fastapi import FastAPI
from models import SongChoice, ClaimedArea, User, GPSPoint

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "This is the base address of the API for managing the location data of the app"}

@app.get("/claimedArea")
async def find_area(location: GPSPoint):
    # TODO probably the hardest math is taking a current location and finding who it overlaps with
    # should return a ClaimedArea object
    return {"message": "This will be a model object"}

@app.post("/claimedArea")
async def claim_area(vertices: set[GPSPoint], song: SongChoice):
    # TODO once you have the locations derive the bounds and get info from the authenticated user
    return {"message": "This is a stub, the objects do not exist"}