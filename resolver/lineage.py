
lineage_data = {}


def record_split(parent_id, children_ids, season, confidence ='High'):
    if parent_id not in lineage_data:
        lineage_data[parent_id] = {}
    
    splits = lineage_data[parent_id].setdefault("splits", [])

    splits.append({
        "season": season,
        "children": children_ids,
        "confidence": confidence
    })

def record_merge(from_ids, to_id, season, confidence='High'):
    for from_id in from_from_ids:
        if from_id not in lineage_data:
            lineage_data[from_id] = {}
        
        merges = lineage_data[from_id].setdefault("merge", [])

        merges.append({
            "season": season,
            "from": from_id,
            "to": to_id,
            "confidence": confidence
        })

def get_lineage(canonical_id):
    return lineage_data.get(canonical_id, {})