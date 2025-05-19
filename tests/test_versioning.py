from shapely.geometry import Polygon
from uuid import uuid4
from resolver import matcher 
from resolver import versioning
import pytest

# import sys
# import os
# sys.path.insert(0, os.path.expanduser("~/dev/ds-projects/canonical_field_resolver"))


def simple_square():
    return {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [0, 0], [0, 1], [1, 1], [1, 0], [0, 0]
                ]]
            }
        }

def test_add_new_version():
    versioning.field_versions.clear()
    new_poly = Polygon(simple_square()["geometry"]["coordinates"][0])

    canonical_id = uuid4()
    matcher.canonical_fields[canonical_id] = new_poly
    
    new_version = versioning.add_new_version(new_poly, canonical_id)

    assert new_version['polygon'] == new_poly
    assert canonical_id in field_versions

#    assert versioning.field_versions.get(canonical_id) ==