import json
import time
from bs4 import BeautifulSoup
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Input and output JSONL file
 # Replace with your actual filename

def scrape_salary_and_location(url):
    """Scrape the salary and location from the job post URL."""
    try:
        time.sleep(3)  # Let the page load
        res = requests.get(url)
        soup = BeautifulSoup(res.content, "html.parser")

        jsonText = soup.find(id="__NEXT_DATA__").text
        jsonData = json.loads(jsonText)

        job_data = jsonData["props"]["pageProps"]["dataSource"]["jobResult"]
        salary = jsonData["props"]["pageProps"]["dataSource"]["jobResult"]["salaryDesc"]
        salary = salary.split(" ")[0]
        location = jsonData["props"]["pageProps"]["dataSource"]["jobResult"]["jobLocation"] 
    
        return salary, location

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return "N/A", "N/A"

def update_jsonl_with_salary_location(file_path):
    # Step 1: Load all objects from file
    updated_objects = []
    with open(file_path, "r", encoding="utf-8") as infile:
        for line in infile:
            try:
                obj = json.loads(line)
                if "url" in obj:
                    updated_objects.append(obj)
            except json.JSONDecodeError:
                print("Skipping invalid JSON line")

    # Step 2: Scrape and update each object in parallel
    with ThreadPoolExecutor(max_workers=30) as executor:
        future_to_obj = {
            executor.submit(scrape_salary_and_location, obj["url"]): obj
            for obj in updated_objects
        }

        for future in as_completed(future_to_obj):
            obj = future_to_obj[future]
            try:
                salary, location = future.result()
                obj["salary"] = salary
                obj["location"] = location
            except Exception as e:
                print(f"Error adding data to object: {e}")
                obj["salary"] = "N/A"
                obj["location"] = "N/A"

    # Step 3: Write back to the same file (overwrite)
    with open(file_path, "w", encoding="utf-8") as outfile:
        for obj in updated_objects:
            json.dump(obj, outfile)
            outfile.write("\n")

    print(f"Updated {len(updated_objects)} objects in {file_path}.")

# ✅ Run it
