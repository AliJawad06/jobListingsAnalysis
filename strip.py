import json
import re

input_file = "additions.jsonl"   # Replace with your input JSONL filename
output_file = "urls.jsonl"  # Replace with your desired output JSONL filename

# Regular expression to match URLs starting with "https" and ending with "1103"
url_pattern = re.compile(r'https\S*1103')

with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
    for line in infile:
        try:
            data = json.loads(line)  # Parse each JSONL line
            url_match = url_pattern.search(json.dumps(data))  # Search for the URL in the JSON string
            if url_match:
                json.dump({"url": url_match.group()}, outfile)  # Write the extracted URL to the new JSONL file
                outfile.write("\n")
        except json.JSONDecodeError:
            print("Skipping invalid JSON line:", line.strip())

print("Extraction completed. URLs saved in", output_file)
