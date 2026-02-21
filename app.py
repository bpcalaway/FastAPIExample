from fastapi import FastAPI
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from datetime import datetime
from models import Turf, User
from gps_utils.area import transform_area_to_gdf

app = FastAPI()
sql_engine = create_engine("postgresql+psycopg2://postgres:postgres@0.0.0.0:5432/killgen_db")
# We're not attaching a db yet, so this just lives in memory while the app runs.  Any restart empties it out
areas = list()


@app.get("/")
async def root():
    return {"message": "This is the base address of the API for managing the location data of the app"}

@app.get("/User")
async def get_users():
    session = Session(sql_engine)
    return User

@app.post("/User")
async def post_user(username: str):
    User.create(name=username)

@app.get("/Turf/")
async def list_turfs():
    print(areas)
    # Currently broken, it relies on having "hashable" data types, points and polygons are not
    return {"areas": areas[0].to_csv()}

@app.post("/Turf/claim")
async def claim_turf(area):
    # TODO once you have the locations derive the bounds and get info from the authenticated user
    #new_area = Turf(verts=vertices, user=current_user, song=song)
    areas.append(area)
    return area

@app.post("/Turf/load")
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
