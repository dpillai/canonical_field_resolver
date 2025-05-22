
lineage_data = {}


def record_split(parent_id, children_ids, season, confidence ='High'):
    if parent_id not in lineage_data:
        lineage_data[parent_id] = {}
    
    splits = lineage_data[parent_id].setdefault("splits", [])

    splits.append({
        "Season": season,
        "Children": children_ids,
        "Confidence": confidence
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