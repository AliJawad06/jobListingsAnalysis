import json

# Input JSONL file containing URLs
input_file = "urls.jsonl"  # Change this to your actual file

# Output Python file
output_file = "urls_list.py"

def extract_urls(input_file):
    """Extracts URLs from a JSONL file and returns them as a list."""
    urls = []
    with open(input_file, "r", encoding="utf-8") as infile:
        for line in infile:
            try:
                data = json.loads(line)
                url = data.get("url")
                if url:
                    urls.append(url)
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON line: {line.strip()}")
    return urls

# Extract URLs and write to a Python file
urls = extract_urls(input_file)

with open(output_file, "w", encoding="utf-8") as outfile:
    outfile.write(f"urls = {json.dumps(urls, indent=4)}\n")

print(f"URLs extracted and saved in {output_file}")
