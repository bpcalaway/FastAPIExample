from models.models import Turf
import geopandas
from geodatasets import get_path
from shapely.geometry import Polygon, mapping
from shapely.wkt import loads

# Determine the actual size of the area in square mileage
# TODO this is the hardest part.  Needs to not claim unclaimable (undecayed) area, and update the vertices so we don't overcompute.  this is probably awful
# Return the total area and the updated vertices as an object
def transform_area_to_gdf(uploaded_filename):
    if not uploaded_filename:
        # TODO remove this, it's for early testing.
        uploaded_filename = "/home/bpcalaway/FastAPIExample/gps_utils/dev_data/mg_cycling_park.geojson"
    gdf = geopandas.read_file(filename=uploaded_filename, driver="GeoJSON", crs='EPSG:4326')
    print(gdf)
    gdf.set_index("name")
    gdf.set_crs(crs="EPSG:6933", allow_override=True)

    gdf['polygon'] = [Polygon(mapping(x)['coordinates']) for x in gdf.geometry]

    gdf["interiors"] = gdf.interiors
    gdf["area_sqkm"] = gdf.area / 10e6 # I don't believe this number at all
    gdf["centroid"] = gdf.centroid # When mapping this it looks like shit, I also don't believe it
    
    gdf = gdf.drop("geometry", axis=1)
    gdf.to_file("src/transform_data/mpls_transform_4_huge.geojson", driver="GeoJSON", index=False)
    print(gdf.columns.to_list())
    print(gdf)
    #gdf.geometry =  gdf['GEOMETRY'].apply(loads)


    return gdf
