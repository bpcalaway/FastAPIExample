from fastapi import APIRouter, UploadFile
from models.models import Turf
from schemas.schemas import TurfSchema
from sqlalchemy import insert, select
import geopandas
from src.area import scale_polygon, intersect, intersect_complex, create_turf_from_gdf
from src.sql import sql_engine
from src.db import get_turf_objects_from_db

router = APIRouter(prefix="/Turf", tags=["Turf"])

@router.get("/") #,response_model=TurfSchema)
async def list_turfs(turf_id: int = None, user_id: int = None):
    """
    Returns a list of turfs based on search criteria, or all turfs if none provided
    """
    conditions = [Turf.protected == False]
    if turf_id:
        conditions.append((Turf.id == turf_id))
    if user_id:
        conditions.append((Turf.user_id == user_id))

    with sql_engine.connect() as conn:
        turfs = conn.execute(select(Turf).filter(*conditions))

    return [dict(r._mapping) for r in turfs]

@router.post("/")
async def claim_turf(turf: UploadFile, user: int):
    """
    Upload a geojson file and create a new entry in the Turf table.  We'll need to keep building this,
    as it is one of our biggest pieces of functionality.  For now, pass it a geojson and a user ID, then
    figure out everything else in the area.py file
    #TODO also create the contested regions while doing this.
    """
    # Only accept valid title geojson files
    if turf.filename[-8:] != ".geojson":
        return {"error": "File not detected as being valid geojson, please check your file upload"}

    gdf = geopandas.read_file(turf.file, driver="GeoJSON", crs='EPSG:4326')
    turf_dict = create_turf_from_gdf(gdf, user)
    with sql_engine.connect() as conn:
        turf_row = conn.execute(insert(Turf).values(**turf_dict))
        conn.commit()

    return {"message": "Successfully uploaded turf"}

@router.get("/transformed_turf")
async def get_transformed_turf(turf_id: int):
    """
    Gets the shape of a turf with all bite sized chunks taken out of it based on its scale at the current moment
    Not every possible_intersections entry will be used, but the logic for finding these will be handled elsewhere
    Will return a single polygon entry that should look like a disaster in most situations.
    """
    possible_intersections = [2, 3] # TODO write the function to find all nearby objects
    #cut_turf(turf_id, possible_intersections())
    print(get_turf_objects_from_db(primary_key=possible_intersections))
    return {"message": "dumbass"}
    

@router.post("/scale_turf")
async def scale_turf(turf_id: int = None):
    """
    Test endpoint, will eventually not need an api call as it will be determined at capture time
    """
    #returns a list but id is unique so should only be one value
    turflist = get_turf_objects_from_db(primary_key=turf_id)

    #get first value from turf list
    turf = turflist[0]
    scaled_pgon = scale_polygon(turf)
    print(scaled_pgon)
    return {"message": "done"}

@router.post("/find_simple_intersection")
async def find_simple_intersection():
    """
    Test Endpoint, will find the intersection of transform_3_large_simple and transform_1_simple
    Notably this will not pay attention to the deterioration of scaled_polygon, yet
    """

    gdf_1 = geopandas.read_file("src/transform_data/mpls_transform_3_large_simple.geojson", driver="GeoJSON")
    gdf_2 = geopandas.read_file("src/transform_data/mpls_transform_6_simple.geojson", driver="GeoJSON")

    inter = intersect(gdf_1, gdf_2)
    return {"message": "done"}

@router.post("/find_complex_single_intersection")
async def find_complex_single_intersection():
    """
    Test endpoint, Works the same as above but a little more complex in that it relies on using the
    intersection of old and new, but also defining the inner scaled polygon as out of bounds for the new
    polygon.  Basically it's the intersection of both - the intersection of the inner polygon
    """
    gdf_1 = geopandas.read_file("src/transform_data/mpls_transform_3_large_simple.geojson", driver="GeoJSON")
    gdf_2 = geopandas.read_file("src/transform_data/mpls_transform_6_simple.geojson", driver="GeoJSON")

    itsverysimpletomeactually = intersect_complex(gdf_1, gdf_2)

    return {"message": "done"}