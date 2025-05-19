from shapely.geometry import Polygon
from shapely.geometry import shape
from uuid import uuid4
from resolver.logger import logger
from resolver import versioning

canonical_fields = {}

def polygon_from_geojson(geojson_feature):
    return shape(geojson_feature['geometry'])

def iou(poly1: Polygon, poly2: Polygon) -> float:
    intersection = poly1.intersection(poly2).area
    union = poly1.union(poly2).area
    return intersection / union if union > 0 else 0.0

def find_best_match(new_poly: Polygon, threshold=0.9):
    for id, can_poly in canonical_fields.items():
        logger.debug(f"Checking IoU to see {id} exists")
        if (iou(new_poly, can_poly) >= threshold):
            logger.info(f"Matching found for {id}")
            return id
    logger.info(f"No Matches found")
    return None

def resolve_field_id(geojson_feature, season=None, source=None):
    new_poly = polygon_from_geojson(geojson_feature)
    id = find_best_match(new_poly)
    if id:
        #CReate the latest servion
        new_version = versioning.add_new_version(new_poly, id, season, source) 
        #Update the field to point to the latest version
        canonical_fields[id] = new_poly
        logger.info(f"Field {id} updated to {new_version['version']}")
        return id
    else:
        new_id = str(uuid4())
        canonical_fields[new_id] = new_poly

        versioning.add_new_version(new_poly, new_id, season, source) 
        logger.info(f"New field {new_id} added to the list")
        return new_id