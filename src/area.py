from models.models import Turf
import geopandas
import topojson as tp
from geodatasets import get_path
from shapely import affinity, force_2d, buffer, intersection, difference
from shapely.geometry import Polygon, mapping
from shapely.wkt import loads
from datetime import datetime

def determine_scale(time: datetime):
    """There's a lot of game logic to still be decided, so a big ol TODO on this one.
        Key thing this function does is determine how much the polygon should have degraded, will return
        a value between -0.0 and -0.5 to see how much of the land is available for contesting
    """
    return -0.002

def scale_polygon(turf: Turf):
    """TODO This should take a polygon as an argument, which will likely be stored as a blob of some kind in the db,
       This will return a scaled polygon, rather than a full db entry or geojson file, eventually.  This is in the test phase
    """
    scale = determine_scale(turf.upload_date)

    pgon = geopandas.GeoSeries.from_wkt(turf.polygon)
    applied_polygon = buffer(pgon, distance=scale, join_style="bevel")

    return applied_polygon

    # Would normally just return this, but we're going to write it to a file
    fname = "src/transform_data/scaled_polygon.geojson"
    new_gdf = geopandas.GeoDataFrame(geometry=applied_polygon)
    new_gdf['polygon'] = [Polygon(mapping(x)['coordinates']) for x in new_gdf.geometry]
    #gdf = gdf.drop("polygon", axis=1)
    new_gdf = new_gdf.drop("geometry", axis=1)
    new_gdf.to_file(fname, driver="GeoJSON", index=False)


def create_turf_from_gdf(gdf: geopandas.geodataframe, user_id: int):
    """
    Create a row in the Turf table and sub entries in ContestedTurfs, from the /Turf post endpoint
    """
    gdf.set_index("name")
    gdf.set_crs(crs="EPSG:6933", allow_override=True)

    # This should plug holes, convert to 2d, and then build a polygon off of the linestring.  SHOULD
    gdf["geometry"] = gdf.geometry.make_valid()
    gdf["geometry"] = force_2d(gdf["geometry"])
    gdf['polygon'] = [Polygon(mapping(x)['coordinates']) for x in gdf.geometry]

    area = gdf.polygon[0].area

     # Simplify really wants this to be a simple triangle, so we're going to try another method using topojson
    topo = tp.Topology(gdf, toposimplify=4)
    gdf = topo.to_gdf()

    gdf.set_geometry(col="polygon", inplace=True)
    point = gdf.centroid[0]

    turf_dict = {
        "user_id": user_id,
        "polygon": str(gdf["polygon"][0]),
        "centroid_lat": point.y,
        "centroid_long": point.x,
        "area_sqkm": area,
        "area_avg_radius": 0.0 #TODO
    }

    return turf_dict


def intersect(existing_gdf: geopandas.geodataframe, new_gdf: geopandas.geodataframe):
    """
    This will eventually get much more complex and involve the intersection of N gdfs, and of their partial decays
    For now, we're hardcoding two and not bothering to decay it.  In short, there's a lot TODO
    """
    pgon1 = geopandas.GeoSeries.from_wkt(existing_gdf["polygon"])
    pgon2 = geopandas.GeoSeries.from_wkt(new_gdf["polygon"])

    inter = intersection(pgon1, pgon2)
    new_gdf = geopandas.GeoDataFrame(geometry=inter)

    # new_gdf["area_sqkm"] = new_gdf.area
    # new_gdf.to_file("src/transform_data/inter_polygon.geojson", driver="GeoJSON", index=False)
    print(new_gdf)

    return new_gdf

def intersect_complex(existing_gdf: geopandas.geodataframe, new_gdf: geopandas.geodataframe):
    """
    Slightly more complex than above, should really only take two args.  Endgame is to take all relevant
    local polygons as an array and find a mix of conflicted areas instead of just the one, but we'll get there

    returns intersection(existing, new) - intersection(inner, new)
    """
    pgon1 = geopandas.GeoSeries.from_wkt(existing_gdf["polygon"])
    pgon2 = scale_polygon(existing_gdf, datetime.now())
    pgon3 = geopandas.GeoSeries.from_wkt(new_gdf["polygon"])

    all_combined = pgon3.intersection(pgon1)
    inner_combined = pgon3.intersection(pgon2)

    print(f"find the diff of {all_combined}")
    print(f"and {inner_combined}")
    
    diff = all_combined.difference(inner_combined)
    print(diff)
    new_gdf = geopandas.GeoDataFrame(geometry=diff)
    new_gdf.to_file("src/transform_data/inter_polygon_debug.geojson", driver="GeoJSON", index=False)

    return None
