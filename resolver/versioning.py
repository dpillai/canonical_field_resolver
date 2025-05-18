from shapely.geometry import Polygon
from shapely.geometry import shape
from uuid import uuid4
from resolver.logger import logger
from resolver import matcher

def polygon_from_geojson(geojson_feature):
    """
    Convert a GeoJSON feature to a Shapely Polygon.
    """
    return shape(geojson_feature['geometry'])

def add_new_version(geojson_feature, field_id, season, source=None):
    """
    Add a new version of a field to the canonical fields.
    """
    new_poly = matcher.polygon_from_geojson(geojson_feature)
    
    new_id = str(uuid4())
    matcher.canonical_fields[new_id] = {
        "polygon": new_poly,
        "version": matcher.canonical_fields[field_id] + 1,
        "source": source,
        "season": season
    }
    return new_id

    