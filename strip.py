import json
import re

def strip(input_file, output_file):
    
    url_pattern = re.compile(r'https\S*1103')
    seen_urls = set()  # To track duplicates

    with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
        for line in infile:
            try:
                data = json.loads(line)
                url_match = url_pattern.search(json.dumps(data))
                if url_match:
                    url = url_match.group()
                    if url not in seen_urls:
                        seen_urls.add(url)
                        json.dump({"url": url}, outfile)
                        outfile.write("\n")
            except json.JSONDecodeError:
                print("Skipping invalid JSON line:", line.strip())

    print("Extraction completed. Unique URLs saved in", output_file)
