from datetime import date
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str
    join: date
    active: bool

class SongChoice(BaseModel):
    # We're just assuming spotify for now
    title: str
    artist: str
    album: str
    pickedBy: User
    spotifyId: int # This will be the lookup for pulling data with the spotify API


class GPSPoint(BaseModel):
    latitude: int
    longitude: int

class ClaimedArea(BaseModel):
    vertices: set # Defined set of GPSPoint objects, use this to define the area specifically

    # The following are used to set a roughly rectangular area for a fast/possibly inaccurate lookup
    northBound: GPSPoint
    southBound: GPSPoint
    westBound: GPSPoint
    eastBound: GPSPoint

    claimedBy: User
    claimedSong: SongChoice
