import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Input and output JSONL files
input_file = "missing_urls.jsonl"
output_file = "output.jsonl"

# CSS class selectors for scraping
skills_selector = "index_qualification-tag__5ZiFf"
title_selector = "index_job-title__sStdA"

# Set up Chrome options for headless browsing
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration for headless mode

# Initialize WebDriver (Make sure to have ChromeDriver installed)
driver = webdriver.Chrome(options=chrome_options)

def scrape_url(url):
    """Scrape the page for job title and skills using Selenium."""
    try:
        driver.get(url)
        time.sleep(5)  # Wait for the page to load (adjust as necessary)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Extract job title
        title_tag = soup.find(class_=title_selector)
        title = title_tag.get_text(strip=True) if title_tag else "N/A"

        # Extract skills
        skill_tags = soup.find_all(class_=skills_selector)
        skills = [tag.get_text(strip=True) for tag in skill_tags]

        return url, title, skills
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return url, "N/A", []

def process_urls():
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
    for url in urls:
        result = scrape_url(url)
        results.append(result)

    # Write results to file
    with open(output_file, "a", encoding="utf-8") as outfile:
        for url, title, skills in results:
            json.dump({"url": url, "title": title, "skills": skills}, outfile)
            outfile.write("\n")

    print(f"Scraping completed. Results saved to {output_file}.")

# Run the function
process_urls()

# Close the WebDriver after scraping is done
driver.quit()
