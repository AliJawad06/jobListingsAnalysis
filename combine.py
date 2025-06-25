import json

def combine(file):
    jobs = []
    with open(file, "r", encoding="utf-8") as infile:
        for line in infile:
            try:
                job = json.loads(line)
                jobs.append(job)
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON line: {line.strip()}")

    
    with open("/Users/alijawad/jobRightScraper/combine.jsonl", "a", encoding="utf-8") as f:
        f.writelines(json.dumps(obj) + "\n" for obj in jobs)

    
repos = ["2025-Business-Analyst-New-Grad","2025-Data-Analysis-New-Grad","2025-Consultant-New-Grad" ,"2025-Management-New-Grad","2025-Product-Management-New-Grad","2025-Software-Engineer-New-Grad",]
path = "Users/alijawad/jobRightScraper/"
for folder in repos:
    file =  folder + "/" + "output.jsonl"
    combine(file)