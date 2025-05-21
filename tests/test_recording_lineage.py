from uuid import uuid4
from resolver import lineage
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



def test_record_split():
    lineage.lineage_data.clear()

    parent_field = uuid4()
    child_one = uuid4()
    child_two = uuid4()

    children_fields = [child_one, child_two]
    
    lineage.record_split(parent_field, children_fields, "2025")

    assert parent_field in lineage.lineage_data

    assert lineage.lineage_data[parent_field]['splits'] == [{
        "season": "2025",
        "children": children_fields,
        "confidence": "High"
    }]

    new_child = uuid4()
    #testing for new plsit being appeded
    lineage.record_split(parent_field, [new_child], "2025")

    assert len(lineage.lineage_data[parent_field]['splits']) == 2