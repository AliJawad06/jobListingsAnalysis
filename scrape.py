import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import requests
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
        res = requests.get(url)
        #print(res.text)
        soup = BeautifulSoup(res.content, "html.parser")
        # Extract job title
        # Extract skills 
        jsonText = soup.find(id="__NEXT_DATA__").text 
        print(jsonText)
        
        jsonData= json.loads(jsonText)
        #print(jsonData)
        jsonSkills = jsonData["props"]["pageProps"]["dataSource"]["jobResult"]["detailQualifications"]["mustHave"]['hardSkill']
        if(len(jsonSkills) == 0):
            jsonSkills = jsonData["props"]["pageProps"]["dataSource"]["jobResult"]["detailQualifications"]["preferredHave"]['hardSkill']
        #print(jsonData["props"]["pageProps"]["dataSource"]["jobResult"]["detailQualifications"]["mustHave"])
        company = jsonData["props"]["pageProps"]["dataSource"]["companyResult"]["companyName"]
        #print(company)
        #print("this is company")
        title = jsonData["props"]["pageProps"]["dataSource"]["jobResult"]["jobTitle"]
        #print(jsonData["props"]["pageProps"]["dataSource"]["jobResult"]["detailQualifications"]["mustHave"])
        #print(jsonSkills)
        print("this is mustHave")
        skills = []
        for skill in jsonSkills:
            print(skill)
            skills.append(skill["skill"])
        return company, url, title, skills
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

    with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust max_workers as needed
        all_results = list(executor.map(scrape_url, urls))
        #results.append(scrape_url(url))
    results.extend(all_results)

    #global driver
   # driver.quit()
    # Write results to file
    with open(output_file, "a", encoding="utf-8") as outfile:
        for company, url, title, skills in results:
            json.dump({"company":company,"url": url, "title": title, "skills": skills}, outfile)
            outfile.write("\n")
   
    print(f"Scraping completed. Results saved to {output_file}.")

# Run the function
#process_urls()

# Close the WebDriver after scraping is done
#driver.quit()