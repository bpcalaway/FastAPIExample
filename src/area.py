from models.models import Turf
import geopandas
import topojson as tp
from geodatasets import get_path
from shapely import affinity, simplify, force_2d, buffer, intersection
from shapely.geometry import Polygon, mapping
from shapely.wkt import loads
from datetime import datetime

def determine_scale(time: datetime):
    """There's a lot of game logic to still be decided, so a big ol TODO on this one.
        Key thing this function does is determine how much the polygon should have degraded, will return
        a value between -0.0 and -0.5 to see how much of the land is available for contesting
    """
    return -0.002

def scale_polygon(gdf: geopandas.geodataframe, capture_time = datetime):
    """TODO This should take a polygon as an argument, which will likely be stored as a blob of some kind in the db,
       This will return a scaled polygon, rather than a full db entry or geojson file, eventually.  This is in the test phase
    """
    scale = determine_scale(capture_time)
    print(f"geo: {gdf.geometry.dtype}, poly: {gdf.polygon.dtype}")
    #pgon = gdf.iloc[0]["polygon"]
    pgon = geopandas.GeoSeries.from_wkt(gdf["polygon"])
    applied_polygon = buffer(pgon, distance=scale, join_style="bevel")
    #scaled_polygon = affinity.scale(pgon, xfact = scale, yfact = scale)

    # Would normally just return this, but we're going to write it to a file
    fname = "src/transform_data/scaled_polygon.geojson"
    gdf["geometry"] = applied_polygon
    #gdf = gdf.drop("polygon", axis=1)
    gdf.to_file(fname, driver="GeoJSON", index=False)

# Determine the actual size of the area in square mileage
# TODO this is the hardest part.  Needs to not claim unclaimable (undecayed) area, and update the vertices so we don't overcompute.  this is probably awful
# Return the total area and the updated vertices as an object
def transform_area_to_gdf(uploaded_filename):
    gdf = geopandas.read_file(filename=uploaded_filename, driver="GeoJSON", crs='EPSG:4326')
    print(gdf)
    gdf.set_index("name")
    gdf.set_crs(crs="EPSG:6933", allow_override=True)

    # This should plug holes, convert to 2d, and then build a polygon off of the linestring.  SHOULD
    gdf["geometry"] = gdf.geometry.make_valid()
    gdf["geometry"] = force_2d(gdf["geometry"])
    gdf['polygon'] = [Polygon(mapping(x)['coordinates']) for x in gdf.geometry]

    # Simplify really wants this to be a simple triangle, so we're going to try another method using topojson
    topo = tp.Topology(gdf, toposimplify=4)
    gdf = topo.to_gdf()
    

    gdf["interiors"] = gdf.interiors
    gdf["area_sqkm"] = gdf.area / 10e6 # I don't believe this number at all
    gdf["centroid"] = gdf.centroid
    
    # You need to drop the original geometry column for mysterious reasons
    gdf = gdf.drop("geometry", axis=1)
    gdf.to_file("src/transform_data/mpls_transform_6_simple.geojson", driver="GeoJSON", index=False)

    return gdf

def intersect(gdf_1: geopandas.geodataframe, gdf_2: geopandas.geodataframe):
    """
    This will eventually get much more complex and involve the intersection of N gdfs, and of their partial decays
    For now, we're hardcoding two and not bothering to decay it.  In short, there's a lot TODO
    """

    inter = intersection(gdf_1.geometry, gdf_2.geometry)
    print(inter)

    return None