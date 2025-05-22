
lineage_data = {}


def record_split(parent_id, children_ids, season, confidence ='High'):
    if parent_id not in lineage_data:
        lineage_data[parent_id] = {}
    
    splits = lineage_data[parent_id].setdefault("split into", [])

    splits.append({
        "Season": season,
        "Children": children_ids,
        "Confidence": confidence
    })

    # Record for each source field
    for child_id in children_ids:
        if child_id not in lineage_data:
            lineage_data[from_id] = {}
        
        origins = lineage_data[from_id].setdefault("split from", [])
        origins.append({
            "season": season,
            "source": parent_id,
            "all_targets": children_ids,  # Full context
            "confidence": confidence
        })

def record_merge(from_ids, to_id, season, confidence='High'):
    # Record for each source field
    for from_id in from_ids:
        if from_id not in lineage_data:
            lineage_data[from_id] = {}
        
        merges = lineage_data[from_id].setdefault("merged_into", [])
        merges.append({
            "season": season,
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
        "sources": from_ids,
        "confidence": confidence
    })

def get_lineage(canonical_id):
    return lineage_data.get(canonical_id, {})