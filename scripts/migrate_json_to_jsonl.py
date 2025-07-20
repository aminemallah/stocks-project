import json

# Input (old) JSON file
old_json_path = "followers_1468103131737247748.json"  # Update with your actual filename

# Output (new) JSONL + meta file
jsonl_path = old_json_path.replace(".json", ".jsonl")
meta_path = old_json_path.replace(".json", ".meta.json")

# Load old JSON data
with open(old_json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

followers = data.get("followers", [])
cursor = data.get("cursor")
total_count = data.get("total_count", len(followers))
last_updated = data.get("last_updated")

# Write to .jsonl
with open(jsonl_path, 'w', encoding='utf-8') as f_jsonl:
    for follower in followers:
        json.dump(follower, f_jsonl, ensure_ascii=False)
        f_jsonl.write('\n')

# Write metadata
metadata = {
    "cursor": cursor,
    "total_count": total_count,
    "last_updated": last_updated
}

with open(meta_path, 'w', encoding='utf-8') as f_meta:
    json.dump(metadata, f_meta, indent=2)

print(f"✅ Migration complete:\n- {len(followers)} followers to {jsonl_path}\n- Metadata saved to {meta_path}")
