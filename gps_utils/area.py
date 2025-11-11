from models import ClaimedArea, GPSPoint
import geopandas
from geodatasets import get_path

# Determine the actual size of the area in square mileage
# TODO this is the hardest part.  Needs to not claim unclaimable (undecayed) area, and update the vertices so we don't overcompute.  this is probably awful
# Return the total area and the updated vertices as an object
def transform_area_to_gdf(uploaded_filename):
    if not uploaded_filename:
        # TODO remove this, it's for early testing.
        uploaded_filename = "/home/bpcalaway/FastAPIExample/gps_utils/dev_data/mg_cycling_park.geojson"
    gdf = geopandas.read_file(filename=uploaded_filename, driver="GeoJSON", crs='EPSG:4326')
    
    gdf.set_index("name")
    gdf.set_crs(crs="EPSG:6933", allow_override=True)
    #gdf = gdf.to_crs("epsg:32633")

    gdf["geometry"] = gdf.geometry.polygonize()
    gdf["interiors"] = gdf.interiors
    gdf["area_sqkm"] = gdf.area / 10e6 # I don't believe this number at all
    gdf["centroid"] = gdf.centroid # When mapping this it looks like shit, I also don't believe it
    print(gdf)

    return gdf