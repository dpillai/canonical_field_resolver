from shapely.geometry import Polygon
from uuid import uuid4
from resolver import matcher
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

def test_ppolygon_conversion():
    poly = matcher.polygon_from_geojson(simple_square())
    assert isinstance(poly, Polygon)

def test_iou():
    poly1 = Polygon(simple_square()["geometry"]["coordinates"][0])
    poly2 = Polygon(simple_square()["geometry"]["coordinates"][0])
    assert matcher.iou(poly1, poly2) == 1.0

def test_resolve_poly_new():
    matcher.canonical_fields.clear()
    field_id = matcher.resolve_field_id(simple_square())
    assert field_id in matcher.canonical_fields


def test_resolve_poly_duplicate():
    matcher.canonical_fields.clear()
    first_field_id = matcher.resolve_field_id(simple_square())
    second_field_id = matcher.resolve_field_id(simple_square())
    assert first_field_id  == second_field_id