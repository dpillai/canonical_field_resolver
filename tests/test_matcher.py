from shapely.geometry import Polygon
from uuid import uuid4
from resolver import matcher, lineage
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
    },
    {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[[0, 0], [0, 1], [1.8, 1], [1.8, 0], [0, 0]]]
        }
    },
       {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[[0, 0], [0, 0.5], [0.5,0.5], [0.5, 0], [0, 0]]]
        }
    }]    

    return polygon_store[int(index)]

def test_ppolygon_conversion():
    poly = matcher.polygon_from_geojson(simple_square(0))
    assert isinstance(poly, Polygon)

def test_iou():
    poly1 = Polygon(simple_square(0)["geometry"]["coordinates"][0])
    poly2 = Polygon(simple_square(0)["geometry"]["coordinates"][0])
    assert matcher.iou(poly1, poly2) == 1.0

def test_resolve_poly_new():
    matcher.canonical_fields.clear()
    field_id = matcher.resolve_field(simple_square(0))
    assert field_id in matcher.canonical_fields


def test_resolve_poly_duplicate():
    matcher.canonical_fields.clear()
    first_field_id = matcher.resolve_field(simple_square(0))
    second_field_id = matcher.resolve_field(simple_square(0))
    assert first_field_id  == second_field_id

def test_canonical_field_points_to_latest_version():

    matcher.canonical_fields.clear()
    first_field_id = matcher.resolve_field(simple_square(0))
    second_field_id = matcher.resolve_field(simple_square(0))
    assert first_field_id  == second_field_id

def test_basic_merge():

    matcher.canonical_fields.clear()
    matcher.field_status.clear()
    lineage.lineage_data.clear()

    field1_id = matcher.resolve_field(simple_square(0))
    field2_id = matcher.resolve_field(simple_square(1))
    merge_field_id = matcher.resolve_field(simple_square(2))

    assert merge_field_id != field1_id
    assert merge_field_id != field2_id
    assert merge_field_id in matcher.canonical_fields
    assert matcher.canonical_fields[merge_field_id] == Polygon(simple_square(2)["geometry"]["coordinates"][0])

def test_field_status_after_merge():

    matcher.canonical_fields.clear()
    matcher.field_status.clear()
    lineage.lineage_data.clear()

    field1_id = matcher.resolve_field(simple_square(0))
    field2_id = matcher.resolve_field(simple_square(1))
    merge_field_id = matcher.resolve_field(simple_square(2))
    
    #Checking status is updated
    assert matcher.field_status[field1_id]["Status"] == "Deprecated"
    assert matcher.field_status[field2_id]["Status"] == "Deprecated"
    assert matcher.field_status[merge_field_id]["Status"] == "Active"

    #Checking Reason is updated
    assert matcher.field_status[field1_id]["Reason"] == f"Merged into {merge_field_id}"
    assert matcher.field_status[field2_id]["Reason"] == f"Merged into {merge_field_id}"

    
def test_lineage_after_merge():

    matcher.canonical_fields.clear()
    matcher.field_status.clear()
    lineage.lineage_data.clear()

    field1_id = matcher.resolve_field(simple_square(0),"2024", "JD")
    field2_id = matcher.resolve_field(simple_square(1), "2024", "NTN")
    merge_field_id = matcher.resolve_field(simple_square(2), "2025", "Owner")
    
    
    assert lineage.lineage_data[field1_id]["merged_into"][0]["all_sources"] == [field1_id, field2_id]
    assert lineage.lineage_data[field1_id]["merged_into"][0]["target"] == merge_field_id
    assert lineage.lineage_data[field2_id]["merged_into"][0]["all_sources"] == [field1_id, field2_id]
    assert lineage.lineage_data[field2_id]["merged_into"][0]["target"] == merge_field_id

    assert lineage.lineage_data[merge_field_id]["merged_from"][0]["sources"] == [field1_id, field2_id]


def test_basic_split():

    matcher.canonical_fields.clear()
    matcher.field_status.clear()
    lineage.lineage_data.clear()

    field1_id = matcher.resolve_field(simple_square(0))
    subfield_id = matcher.resolve_field(simple_square(3))

    assert subfield_id != field1_id
    assert subfield_id in matcher.canonical_fields
    assert matcher.canonical_fields[subfield_id] == Polygon(simple_square(3)["geometry"]["coordinates"][0])


def test_field_status_after_split():

    matcher.canonical_fields.clear()
    matcher.field_status.clear()
    lineage.lineage_data.clear()

    field1_id = matcher.resolve_field(simple_square(0))
    subfield_id = matcher.resolve_field(simple_square(3))
    
    #Checking status is updated
    assert matcher.field_status[field1_id]["Status"] == "Active"
    assert matcher.field_status[subfield_id]["Status"] == "Active"

    #Checking Reason is updated
    assert matcher.field_status[subfield_id]["Reason"] == f"New field {subfield_id} split from {field1_id}"

def test_lineage_after_split():

    matcher.canonical_fields.clear()
    matcher.field_status.clear()
    lineage.lineage_data.clear()

    field1_id = matcher.resolve_field(simple_square(0))
    subfield_id = matcher.resolve_field(simple_square(3))
    
    assert lineage.lineage_data[field1_id]["split_into"][0]["children"] == [subfield_id]
    assert lineage.lineage_data[subfield_id]["split_from"][0]["source"] == [field1_id]
