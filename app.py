from fastapi import FastAPI
from datetime import datetime
from models import SongChoice, ClaimedArea, User, GPSPoint
from gps_utils.area import transform_area_to_gdf

app = FastAPI()

# We're not attaching a db yet, so this just lives in memory while the app runs.  Any restart empties it out
areas = list()


@app.get("/")
async def root():
    return {"message": "This is the base address of the API for managing the location data of the app"}

@app.get("/claimedArea/")
async def list_areas():
    print(areas)
    # Currently broken, it relies on having "hashable" data types, points and polygons are not
    return {"areas": areas[0].to_csv()}

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

@app.post("/claimedArea/load")
async def load_sample_files():
    # TODO remove this, it's for local testing and loads a bunch of my nonsense files
    files = [
        #"/home/bpcalaway/FastAPIExample/gps_utils/dev_data/mg_cycling_park.geojson",
        #"/home/bpcalaway/FastAPIExample/gps_utils/dev_data/devils_lake_hike.geojson",
        #"/home/bpcalaway/FastAPIExample/gps_utils/dev_data/east_loi_brady_home.geojson",
        #"/home/bpcalaway/FastAPIExample/gps_utils/dev_data/michigan_north_shore.geojson",
        "gps_utils/dev_data/msp_light_overlap.geojson"
    ]
    for file in files:
        gdf = transform_area_to_gdf(file)
        areas.append(gdf)
