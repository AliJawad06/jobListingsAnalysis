import sys
from datetime import datetime
from zutils.getOldListings import * 
from zutils.scrape import *
from zutils.strip import * 
from zutils.toCSV import*
from zutils.combine import*

def main():
    repos = ["2025-Business-Analyst-New-Grad","2025-Data-Analysis-New-Grad","2025-Consultant-New-Grad" ,"2025-Management-New-Grad","2025-Product-Management-New-Grad","2025-Software-Engineer-New-Grad",]
    #repos = ["2025-Consultant-New-Grad"]
    path = "/Users/alijawad/jobRightScraper/" 
        
    #for folder in repos:
        #file_path = "README.md"
        #additions_output = "additions.jsonl"
        #commit_tracker = "last_commit.jsonl"
        ##os.chdir(path + folder)
        #process_new_commits(file_path, additions_output, commit_tracker,folder)
        #strip(input_file="additions.jsonl", output_file="urls.jsonl")
        #process_urls(input_file="urls.jsonl",output_file="output.jsonl")
        #combine_path = path + folder + '/output.jsonl'
        #append_jsonl_to_jsonl(combine_path, path + "combine.jsonl")
    jsonl_to_csv(path + "combine.jsonl", path + "combine.csv")

            



        
if __name__ == "__main__":
    main()
        

    






