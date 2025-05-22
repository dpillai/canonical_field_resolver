from shapely.geometry import Polygon
from shapely.geometry import shape
from uuid import uuid4
from resolver.logger import logger
from resolver import versioning, lineage

EPSILON = 1e-6
canonical_fields = {}
field_status = {} # Maps canonical_id to Status

def polygon_from_geojson(geojson_feature):
    return shape(geojson_feature['geometry'])

def iou(poly1: Polygon, poly2: Polygon) -> float:
    intersection = poly1.intersection(poly2).area
    union = poly1.union(poly2).area
    return intersection / union if union > 0 else 0.0

def find_matches(new_poly: Polygon, iou_thresh=0.8, containment_thresh=0.9):
    field_to_be_versioned = []
    fields_to_be_merged = []
    field_to_be_split = []

    for fid, can_poly in canonical_fields.items():

        iou_score = iou(new_poly, can_poly)
        intersection_area = new_poly.intersection(can_poly).area
        containment_old_in_new = intersection_area / can_poly.area if can_poly.area > 0 else 0
        containment_new_in_old = intersection_area / new_poly.area

        if iou_score >= iou_thresh:
            field_to_be_versioned.append(fid)
        elif iou_score < 0.5 and abs(intersection_area - new_poly.area) < EPSILON:
            field_to_be_split.append(fid)
        elif containment_old_in_new >= containment_thresh or containment_new_in_old >= containment_thresh:
            fields_to_be_merged.append(fid)
            
    return field_to_be_versioned, fields_to_be_merged, field_to_be_split

def resolve_field(geojson_feature, season=None, source=None):

    """
    Resolves a GeoJSON field by either:
    1. Creating a new field if no match is found
    2. Updating an existing field if a high match is found
    3. Creating a merged field if partial containment is found
    
    Merging process:
    - When a new field has significant containment with existing fields
    - A new canonical ID is created
    - Original fields are marked as 'Deprecated'
    - Lineage information is recorded
    
    Args:
        geojson_feature: GeoJSON Feature with Polygon geometry
        season: Optional season identifier
        source: Optional source identifier
        
    Returns:
        UUID of the resolved field
    """
    new_poly = polygon_from_geojson(geojson_feature)
    
    if new_poly.area == 0 or not new_poly.is_valid:
        logger.warning("Rejected invalid or zero-area polygon.")
        return None
    
    field_to_be_versioned, fields_to_be_merged, field_to_be_split = find_matches(new_poly)

    if not (field_to_be_versioned or fields_to_be_merged or field_to_be_split):
     
        new_id = str(uuid4())
        canonical_fields[new_id] = new_poly
        versioning.add_new_version(new_poly, new_id, season, source)
        logger.info(f"New field {new_id} added.")

        field_status[new_id] = {
            "Status": "Active",
            "Reason": f"New field {new_id} added"
        }
        return new_id

    elif field_to_be_versioned:
        fid = field_to_be_versioned[0]
        new_version = versioning.add_new_version(new_poly, fid, season, source)
        canonical_fields[fid] = new_poly
        logger.info(f"Field {fid} updated to version {new_version['version']}")
        return fid

    elif field_to_be_split:
        new_id = str(uuid4())
        canonical_fields[new_id] = new_poly
        versioning.add_new_version(new_poly, new_id, season, source)
        logger.info(f"New field {new_id} added.")

        field_status[new_id] = {
            "Status": "Active",
            "Reason": f"New field {new_id} split from {field_to_be_split[0]}"
        }
        lineage.record_split(field_to_be_split[0], [new_id], season, source)
        return new_id
    else:
        # Merge scenario
        new_id = str(uuid4())
        canonical_fields[new_id] = new_poly
        lineage.record_merge(fields_to_be_merged, new_id, season)
        versioning.add_new_version(new_poly, new_id, season, source)
        logger.info(f"New merged field {new_id} from {fields_to_be_merged}")

        # Make an entry in field_status for the new merged field
        field_status[new_id] = {
            "Status": "Active",
            "Reason": f"New field {new_id} added"
        }
        #Update Status of old fields to Deprecated post merge
        for field in fields_to_be_merged:
            field_status[field] = {
                "Status": "Deprecated",
                "Reason": f"Merged into {new_id}"
            }
        return new_id


def get_field_status(field_id):
    """Returns the status of a field or 'Active' if not explicitly set."""
    return field_status.get(field_id, 'Active')