import json
import os

def update_jsonl_with_field(jsonl_file):
    updated_lines = []

    # Read and process each line
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                obj = json.loads(line)
                url = obj.get("url", "")
                if "=" in url and "&" in url:
                    field_val = url.split("=", 1)[1].split("&", 1)[0].replace("%20", " ")
                    obj["field"] = field_val
                updated_lines.append(json.dumps(obj))
            except Exception as e:
                print(f"Skipping line due to error: {e}")

    # Overwrite file with updated content
    with open(jsonl_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(updated_lines) + '\n')

# 🔁 Run it
update_jsonl_with_field("combine.jsonl")
