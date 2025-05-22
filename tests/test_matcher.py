from shapely.geometry import Polygon
from uuid import uuid4
from resolver import matcher
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
