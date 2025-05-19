from shapely.geometry import Polygon
from uuid import uuid4
from resolver import matcher, versioning 
import pytest

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
    
    new_version = versioning.add_new_version(new_poly, canonical_id, None, None)

    assert new_version['polygon'] == new_poly
    assert canonical_id in versioning.field_versions

    # First version should be 'v1'
    assert versioning.field_versions.get(canonical_id)[0]['version'] == "v1"


    second_poly = Polygon(simple_square()["geometry"]["coordinates"][0])
    second_version = versioning.add_new_version(second_poly, canonical_id, None, None)

    # Second version should be 'v2' and update the canonical polygon
    assert versioning.field_versions.get(canonical_id)[1]['version'] == "v2"
    assert matcher.canonical_fields[canonical_id].equals(second_poly)