import json
from collections import Counter

# Input JSONL file
input_file = "output.jsonl"

# Dictionary to count skill occurrences
skill_counter = Counter()

# Read the JSONL file and count skills
with open(input_file, "r", encoding="utf-8") as infile:
    for line in infile:
        try:
            data = json.loads(line)
            skills = data.get("skills", [])
            skill_counter.update(skills)
        except json.JSONDecodeError:
            print(f"Skipping invalid JSON line: {line.strip()}")

# Get the top 30 most frequent skills
top_skills = skill_counter.most_common(200)

# Print the top skills
print("Top 30 Most Frequent Skills:")
for skill, count in top_skills:
    print(f"{skill}: {count}")
