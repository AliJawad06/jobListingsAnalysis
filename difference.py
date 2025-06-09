import json

def get_urls_from_jsonl(file_path):
    """Extract URLs from a JSONL file and return them as a set."""
    urls = set()
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            try:
                data = json.loads(line)
                if "url" in data:
                    urls.add(data["url"].rstrip("/"))  # Normalize by removing trailing slashes
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON line: {line.strip()}")
    return urls

def find_missing_urls(file1, file2, output_file):
    """Find URLs in file1 that are NOT in file2 and save them to a new JSONL file."""
    urls_file1 = get_urls_from_jsonl(file1)
    urls_file2 = get_urls_from_jsonl(file2)

    missing_urls = urls_file1 - urls_file2  # URLs in file1 but not in file2

    with open(output_file, "w", encoding="utf-8") as outfile:
        for url in missing_urls:
            json.dump({"url": url}, outfile)
            outfile.write("\n")

    print(f"Missing URLs saved to {output_file}")

# Example usage
file1 = "urls.jsonl"   # Replace with actual file path
file2 = "output.jsonl"  # Replace with actual file path
output_file = "missing_urls.jsonl"    # Output file for differences

find_missing_urls(file1, file2, output_file)
