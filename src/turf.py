from fastapi import APIRouter, UploadFile
from models.models import Turf
from schemas.schemas import TurfSchema
from sqlalchemy import insert, select
import geopandas
from src.area import scale_polygon, intersect, intersect_complex, create_turf_from_gdf
from src.sql import sql_engine

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

@router.post("/scale_turf")
async def scale_turf():
    """
    Test endpoint, will eventually not need an api call as it will be determined at capture time
    """
    test_data = "src/transform_data/mpls_transform_3_large_simple.geojson"
    gdf = geopandas.read_file(filename=test_data, driver="GeoJSON")
    print(gdf)
    scale_polygon(gdf)

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