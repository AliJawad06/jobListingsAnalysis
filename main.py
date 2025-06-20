import sys
from datetime import datetime


from getOldListngs import * 
from difference import *
from scrape import *
from strip import * 

def main():
    repos = ["2025-Business-Analyst-New-Grad","2025-Management-New-Grad"]

    for folder in repos:
        file_path = "README.md"
        additions_output = "additions.jsonl"
        commit_tracker = "last_commit.jsonl"

        process_new_commits(file_path, additions_output, commit_tracker,folder)


        input_file = "additions.jsonl"   # Replace with your input JSONL filename
        output_file = "urls.jsonl"  # Replace with your desired output JSONL filename

        strip(input_file="additions.jsonl", output_file="urls.jsonl")

        delta = 1

        while(delta != 0): 
            

    # Set up Chrome options for headless browsing
            # Disable GPU acceleration for headless mode

    # Initialize WebDriver (Make sure to have ChromeDriver installed)


            process_urls(input_file="urls.jsonl",output_file="output.jsonl")
            # Close the WebDriver after scraping is done

            file1 = "urls.jsonl"   # Replace with actual file path
            file2 = "output.jsonl"  # Replace with actual file path
            output_file = "missing_urls.jsonl"    # Output file for differences

            difference = find_missing_urls(file1 = "urls.jsonl" , file2 ="output.jsonl"  , output_file= "missing_urls.jsonl") 

            delta = delta - difference - 1



        
if __name__ == "__main__":
    main()
        

    






