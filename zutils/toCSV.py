import traceback
import json
import csv
from difflib import SequenceMatcher

def jsonl_to_csv(input_jsonl_file, output_csv_file):
    data = []
    with open(input_jsonl_file, 'r', encoding='utf-8') as f_in:
        for line in f_in:
            try:
                job = json.loads(line)
                salary = job.get("salary", "")

                if not isinstance(salary, str) or not salary:
                    job["salary"] = "N/A"
                    data.append(job)
                    continue

                ending = salary[-3:]

                if ending == "/hr":
                    cleaned = salary.replace("$", "").replace("/hr", "")
                    hourly = float(cleaned)
                    yearly = round(hourly * 40 * 52)
                    job["salary"] = yearly

                elif salary == "$0/yr":
                    job["salary"] = "N/A"

                elif ending == "/yr":
                    cleaned = salary.replace("$", "").replace("K", "000").replace("/yr", "")
                    yearly = float(cleaned)
                    job["salary"] = yearly

                elif ending == "/mo":
                    cleaned = salary.replace("$", "").replace("/mo", "").replace(",", "")
                    yearly = float(cleaned) * 12
                    job["salary"] = yearly
                else:
                    job["salary"] = "N/A"
                
                data.append(job)
            except Exception:
                print("Error parsing line:")
                traceback.print_exc()
                continue  #
         

        
    # Determine header from the keys of the first JSON object
        fieldnames = data[0].keys()

        with open(output_csv_file, 'w', newline='', encoding='utf-8') as f_out:
            writer = csv.DictWriter(f_out, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)


