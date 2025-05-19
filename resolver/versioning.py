from shapely.geometry import Polygon
from shapely.geometry import shape
from uuid import uuid4
from resolver.logger import logger

field_versions = {}

def add_new_version(new_poly, canonical_id, season, source=None):
 
    current_versions = field_versions.get(canonical_id, [])
    new_version_id = f"v{len(current_versions)+1}"

    new_version = {
        "version": new_version_id,
        "polygon": new_poly,
        "season": season,
        "source": source
    }

    field_versions.setdefault(canonical_id,[]).append(new_version)
    logger.info(f"Version {new_version['version']} added for field {canonical_id}")
    return new_version