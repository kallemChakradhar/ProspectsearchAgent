import json
import os
from techstack_api import fetch_tech_stack

def merge_and_deduplicate(apollo_data, crunchbase_data):
    merged = {}
    def key(c):
        return (c.get("domain") or c.get("company_name")).lower() if (c.get("domain") or c.get("company_name")) else None

    for c in crunchbase_data + apollo_data:
        k = key(c)
        if not k:
            continue
        if k in merged:
            merged[k]["signals"].update(c.get("signals", {}))
            if c.get("contacts"):
                if merged[k].get("contacts") is None:
                    merged[k]["contacts"] = c["contacts"]
                else:
                    merged[k]["contacts"].extend(c["contacts"])
            merged[k]["source"] = list(set(merged[k]["source"] + c.get("source", [])))
            merged[k]["confidence"] = round((merged[k]["confidence"] + c.get("confidence", 0.85))/2, 2)
        else:
            merged[k] = c

    final_list = list(merged.values())
    return final_list

def save_to_json(data, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Final merged results saved to {filepath}")
