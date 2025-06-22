import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests


try:
        
        headers = {
        "User-Agent": "Mozilla/5.0"
        }
    #    driver.get(url)
        time.sleep(5)  # Wait for the page to load (adjust as necessary)
        res = requests.get("https://jobright.ai/jobs/info/683748c9dbf0418b9288deda?utm_campaign=Management%20and%20Executive&utm_source=1103",headers=headers)
        #print(res.text)
        time.sleep(3)
                
        soup = BeautifulSoup(res.text, "html.parser")

        # Find the span by class (you can use just part of the class name or the full list)
        span = soup.select_one("span.index_expires-in__02frg")
        if span:
            print(span.get_text())


       
  
        
except Exception as e:
        print(f"Error fetching {e} ")
        