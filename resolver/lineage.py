
lineage_data = {}


def record_split(parent_id, children_ids, season=None, source=None, confidence ='High'):
    if parent_id not in lineage_data:
        lineage_data[parent_id] = {}
    
    splits = lineage_data[parent_id].setdefault("split_into", [])

    splits.append({
        "season": season,
        "source": source,
        "children": children_ids,
        "confidence": confidence
    })

    # Record for each source field
    for child_id in children_ids:
        if child_id not in lineage_data:
            lineage_data[child_id] = {}
        
        origins = lineage_data[child_id].setdefault("split_from", [])
        origins.append({
            "season": season,
            "source": source,
            "parent": parent_id,
            "all_children": children_ids,  # Full context
            "confidence": confidence
        })

def record_merge(from_ids, to_id, season=None, source=None, confidence='High'):
    # Record for each source field
    for from_id in from_ids:
        if from_id not in lineage_data:
            lineage_data[from_id] = {}
        
        merges = lineage_data[from_id].setdefault("merged_into", [])
        merges.append({
            "season": season,
            "source": source,
            "target": to_id,
            "all_sources": from_ids,  # Full context
            "confidence": confidence
        })
    
    # Record for target field
    if to_id not in lineage_data:
        lineage_data[to_id] = {}
    
    origins = lineage_data[to_id].setdefault("merged_from", [])
    origins.append({
        "season": season,
        "source": source,
        "sources": from_ids,
        "confidence": confidence
    })

def get_lineage(canonical_id):
    return lineage_data.get(canonical_id, {})