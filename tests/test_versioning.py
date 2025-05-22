from shapely.geometry import Polygon
from uuid import uuid4
from resolver import matcher, versioning 
import pytest

def simple_square(index):

    polygon_store = [
        {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]
        }
    },    
    {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[[0.8, 0], [0.8, 1], [1.8, 1], [1.8, 0], [0.8, 0]]]
        }
    }]
        
    return polygon_store[int(index)]  


def test_add_new_version():
    versioning.field_versions.clear()
    new_poly = Polygon(simple_square(0)["geometry"]["coordinates"][0])

    canonical_id = uuid4()
    matcher.canonical_fields[canonical_id] = new_poly
    
    new_version = versioning.add_new_version(new_poly, canonical_id, "2025", "NTN")

    assert new_version['polygon'] == new_poly
    assert canonical_id in versioning.field_versions

    # First version should be 'v1'
    assert versioning.field_versions.get(canonical_id)[0]['version'] == "v1"


    duplicate_poly = Polygon(simple_square(0)["geometry"]["coordinates"][0])
    duplicate_version = versioning.add_new_version(duplicate_poly, canonical_id, "2025", "JD")

    # Duplicate field should not increment version and just add observations
    print(versioning.field_versions.get(canonical_id)[-1]["observations"])
    assert duplicate_version["observations"] == [{"season": "2025", "source": "JD"}]
    assert duplicate_version["version"] == "v1"
 
 
     # Second version should be 'v2' and update the canonical polygon
    second_poly = Polygon(simple_square(1)["geometry"]["coordinates"][0])
    second_field_id = uuid4()
    second_poly_version = versioning.add_new_version(second_poly, second_field_id, "2025", "JD")
    assert versioning.field_versions.get(second_field_id)[0]['version'] == "v1"


    assert len(versioning.field_versions) == 2