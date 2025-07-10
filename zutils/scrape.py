import requests
import time
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor, as_completed




def scrape_url(url):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.content, "html.parser")
        jsonText = soup.find(id="__NEXT_DATA__").text
        jsonData = json.loads(jsonText)

        job_data = jsonData["props"]["pageProps"]["dataSource"]["jobResult"]
        company_data = jsonData["props"]["pageProps"]["dataSource"]["companyResult"]

        qualifications = job_data.get("detailQualifications", {})
        must_have = qualifications.get("mustHave", {}).get("hardSkill", [])
        preferred = qualifications.get("preferredHave", {}).get("hardSkill", [])

        jsonSkills = must_have or preferred

        company = company_data.get("companyName", "N/A")
        title = job_data.get("jobTitle", "N/A")
        date = job_data.get("publishTime","N/A").split(" ")[0]
        recruiter = job_data.get("jobRecruiter","N/A")
        salary = job_data.get("salaryDesc", "N/A").split(" ")[0]
        #company, date, salary, url, title, skills, recruiter, location, 
        location = job_data.get("jobLocation", "N/A")
        skills = [s.get("skill", "") for s in jsonSkills]

        return company, date,salary,url, title, skills, recruiter, location

    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return "N/A", url, "N/A", []



def process_urls(input_file,output_file):
    # Set up Chrome options for headless browsing
     # Disable GPU acceleration for headless mode

# Initialize WebDriver (Make sure to have ChromeDriver installed)

    
    """Process each URL in the input file and scrape with Selenium."""
    urls = []
    with open(input_file, "r", encoding="utf-8") as infile:
        for line in infile:
            try:
                data = json.loads(line)
                if "url" in data:
                    urls.append(data["url"])
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON line: {line.strip()}")
    # Scrape URLs one by one
    results = []
    #for url in urls:
    with open(output_file, "a", encoding="utf-8") as outfile, open("missing_urls.jsonl", 'a', encoding='utf-8') as errfile:
        with ThreadPoolExecutor(max_workers=10) as executor: 
            future_to_url = {executor.submit(scrape_url, url): url for url in urls}
            for future in as_completed(future_to_url):  # global timeout
                url = future_to_url[future]
                try:
                    result = future.result()  # per-task timeout
                    company, date, salary, url, title, skills, recruiter,location = result
                    print(f"Success: {url}")
                    json.dump({
                        "company": company or "N/A",
                        "date": date  or "N/A",
                        "salary": salary or "N/A",
                        "url": url or "N/A",
                        "title": title or "N/A",
                        "skills": skills or "N/A",
                        "recruiter": recruiter or "N/A", 
                        "location": location  or "N/A"
                    }, outfile)
                    outfile.write("\n")
                except Exception as e:
                    json.dump({
                        "url": url
                    },errfile)
                    errfile.write("\n")
                    
   
    print(f"Scraping completed. Results saved to {output_file}.")

