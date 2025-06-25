import sys
from datetime import datetime


from getOldListngs import * 
from difference import *
from scrape import *
from strip import * 
from update import *
from toCSV import*

def main():
    #repos = ["2025-Business-Analysis-New-Grad","2025-Data-Analysis-New-Grad","2025-Consultant-New-Grad" ,"2025-Management-New-Grad","2025-Product-Management-New-Grad","2025-Software-Engineer-New-Grad",]
    repos = ["2025-Consultant-New-Grad"]
    path = "/Users/alijawad/jobRightScraper/" 
        
    for folder in repos:
        os.chdir(path + folder)
        file_path = "README.md"
        additions_output = "additions.jsonl"
        commit_tracker = "last_commit.jsonl"
        #process_new_commits(file_path, additions_output, commit_tracker,folder)
        #strip(input_file="additions.jsonl", output_file="urls.jsonl")
        process_urls(input_file="urls.jsonl",output_file="output.jsonl")
        #Close the WebDriver after scraping is done
        #update_jsonl_with_salary_location("output.jsonl")
        difference = find_missing_urls(file1 = "urls.jsonl" , file2 ="output.jsonl"  , output_file= "missing_urls.jsonl") 
        combine("ouput.jsonl")
    jsonl_to_csv("combine.jsonl", "combine.csv")

            



        
if __name__ == "__main__":
    main()
        

    






