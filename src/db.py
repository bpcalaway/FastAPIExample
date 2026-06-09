from shapely import from_wkt
from models.models import Turf
from sqlalchemy import insert, select
from src.sql import sql_engine
import geopandas

def _serialize_row_objects(db_results):
    """
    Gets a list of cursors and dumps them to a list of dictionaries
    """
    serialized_objects = list()
    for result in db_results:
        map = dict(result._mapping)
        if "polygon" in map.keys():
            map["polygon"] = from_wkt(str(map["polygon"]))
        serialized_objects.append(map)

    return serialized_objects

def get_turf_objects_from_db(primary_key: int | list[int]) -> list:
    """
    Send either a primary key or a list of primary keys and return a list of Turf objects as
    dictionaries.  Each of these will be serialized for ease of use
    """
    if type(primary_key) == int:
        sql = select(Turf).where(Turf.id==primary_key)
    else:
        sql = select(Turf).filter(Turf.id.in_(primary_key))
    with sql_engine.connect() as conn:
        results = conn.execute(sql)

    return _serialize_row_objects(results)
