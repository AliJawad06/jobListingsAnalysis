import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import os


# Input and output JSONL files
#input_file = "missing_urls.jsonl"
#output_file = "output.jsonl"

# CSS class selectors for scraping
#skills_selector = "index_qualification-tag__5ZiFf"
#title_selector = "index_job-title__sStdA"

# Set up Chrome options for headless browsing
#chrome_options = Options()
#chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration for headless mode

# Initialize WebDriver (Make sure to have ChromeDriver installed)
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
#driver = webdriver.Chrome(options=chrome_options)

def scrape_url(url):
    
   # global driver
    skills_selector = "index_qualification-tag__5ZiFf"
    title_selector = "index_job-title__sStdA"
    """Scrape the page for job title and skills using Selenium."""
    try:
    #    driver.get(url)
        time.sleep(5)  # Wait for the page to load (adjust as necessary)
        res = requests.get("https://jobright.ai/jobs/info/685213ffb601b8126382fd6b?utm_campaign=Consultant&utm_source=1103")
        soup = BeautifulSoup(res.content, "html.parser")

        jsonText = soup.find(id="__NEXT_DATA__").text 
        jsonData = json.loads(jsonText)

        data_source = jsonData.get("props", {}).get("pageProps", {}).get("dataSource", {})
        job_result = data_source.get("jobResult", {})
        company_result = data_source.get("companyResult", {})

        # Skills
        jsonSkills = job_result.get("detailQualifications", {}).get("mustHave", {}).get("hardSkill", [])
        if not jsonSkills:
            jsonSkills = job_result.get("detailQualifications", {}).get("preferredHave", {}).get("hardSkill", [])

        # Company
        company = company_result.get("companyName", "N/A")

        # Title
        title = job_result.get("jobTitle", "N/A")

        # Date
        date = job_result.get("publishTime", "").split(" ")[0] if job_result.get("publishTime") else "N/A"

        # Salary
        salary_desc = job_result.get("salaryDesc", "")
        salary = salary_desc.split(" ")[0] if salary_desc else "N/A"

        # Recruiter
        recruiter = job_result.get("jobRecruiter", "") or "N/A"

        # Location
        location = job_result.get("jobLocation", "N/A")

        skills = []
        for skill in jsonSkills:
            skills.append(skill["skill"])
        return company, date,salary,url, title, skills, recruiter,location
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return url, "N/A", []


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
    with open(output_file, "a", encoding="utf-8") as outfile:
        with ThreadPoolExecutor(max_workers=10) as executor: 
            future_to_url = {executor.submit(scrape_url, url): url for url in urls}
            for future in as_completed(future_to_url, timeout=60):  # global timeout
                url = future_to_url[future]
                try:
                    result = future.result(timeout=30)  # per-task timeout
                    company, date,salary,url, title, skills, recruiter, location = result
                    print(f"Success: {url}")
                    field = os.getcwd().replace("/Users/alijawad/jobRightScraper", "").replace("2025-", "").replace("-New-Grad","")
                    json.dump({
                        "company": company,
                        "date": date,
                        "salary": salary,
                        "url": url,
                        "title": title,
                        "skills": skills,
                        "recruiter": recruiter,
                        "location": location,
                        "field": field
                    }, outfile)
                    outfile.write("\n")
                except Exception as e:
                    print(f"Error scraping {url}: {e}")
   
    print(f"Scraping completed. Results saved to {output_file}.")

# Run the function
#process_urls()

# Close the WebDriver after scraping is done
#driver.quit()