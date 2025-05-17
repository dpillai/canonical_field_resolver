from shapely.geometry import Polygon
from shapely.geometry import shape
from uuid import uuid4


canonical_fields = {}

def polygon_from_geojson(geojson_feature):
    return shape(geojson_feature['geometry'])

def iou(poly1: Polygon, poly2: Polygon) -> float:
    intersection = poly1.intersection(poly2).area
    union = poly1.union(poly2).area
    return intersection / union if union > 0 else 0.0

def find_best_match(new_poly: Polygon, threshold=0.9):
    for id, can_poly in canonical_fields.items():
        if (iou(new_poly, can_poly) >= threshold):
            return id
    return None

def resolve_field_id(geojson_feature):
    new_poly = polygon_from_geojson(geojson_feature)
    id = find_best_match(new_poly)
    if id:
        return id
    else:
        new_id = str(uuid4())
        canonical_fields[new_id] = new_poly
        return new_id

 
