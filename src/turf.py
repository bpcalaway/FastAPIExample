from fastapi import APIRouter
from models.models import Turf
from schemas.schemas import TurfSchema
import geopandas
from src.area import transform_area_to_gdf, scale_polygon, intersect

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

@router.post("/transform_turf")
async def transform_turf():
    """
    Test endpoint to load a file from dev_data and try to transform it
    """
    test_data = "src/dev_data/east_loi_brady_home.geojson"
    gdf = transform_area_to_gdf(test_data)

    return {"message": "hello"} #str(gdf.polygon[0])}

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
    gdf_2 = geopandas.read_file("src/transform_data/mpls_transform_1_simple.geojson", driver="GeoJSON")

    intersect(gdf_1, gdf_2)

    return {"message": "done"}