import requests
from bs4 import BeautifulSoup
import json

res = requests.get("https://jobright.ai/jobs/info/685213ffb601b8126382fd6b?utm_campaign=Consultant&utm_source=1103")
soup = BeautifulSoup(res.content, "html.parser")

jsonText = soup.find(id="__NEXT_DATA__").text 
jsonData = json.loads(jsonText)

data_source = jsonData.get("props", {}).get("pageProps", {}).get("dataSource", {})
job_result = data_source.get("jobResult", {})
company_result = data_source.get("companyResult", {})

# Skills
skills = job_result.get("detailQualifications", {}).get("mustHave", {}).get("hardSkill", [])
if not skills:
    skills = job_result.get("detailQualifications", {}).get("preferredHave", {}).get("hardSkill", [])

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

# Debug output (you can remove these in production)
print("Company:", company)
print("Title:", title)
print("Date:", date)
print("Salary:", salary)
print("Recruiter:", recruiter)
print("Location:", location)
print("Skills:", skills)
