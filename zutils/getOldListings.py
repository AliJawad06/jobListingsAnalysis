import subprocess
import json
import os




def pull_latest(repo): 
    try:
        path = "/Users/alijawad/jobRightScraper/" 
        os.chdir(path + repo)
        print(os.getcwd()) 
        result2 = subprocess.run(["git", "pull"],
                                capture_output=True, text=True, check=True)  
       

    except subprocess.CalledProcessError as e:
        print("Exception on process, rc=", e.returncode, "output=", e.output)


def get_all_commit_hashes(file_path):
    """Get all commit hashes for a file, most recent first."""
    result = subprocess.run(
        ["git", "log", "--format=%H", "-n","100", "--",  file_path],
        capture_output=True, text=True, check=True
    )
    return result.stdout.strip().split("\n")

def get_last_scraped_commit(scrape_meta_path):
    """Read last scraped commit from JSONL file."""
    try:
        with open(scrape_meta_path, "r", encoding="utf-8") as f:
            return json.loads(f.readline())["last_scraped_commit"]
    except Exception:
        return None

def update_scraped_commit(scrape_meta_path, commit_hash):
    """Overwrite JSONL with latest commit hash."""
    with open(scrape_meta_path, "w", encoding="utf-8") as f:
        json.dump({"last_scraped_commit": commit_hash}, f)
        f.write("\n")

def get_commit_diff(commit_hash, file_path):
    """Get lines added in a specific commit for a file."""
    result = subprocess.run(
        ["git", "show", commit_hash, "--", file_path],
        capture_output=True, text=True, check=True
    )
    additions = []
    for line in result.stdout.splitlines():
        if line.startswith('+') and not line.startswith('+++'):
            additions.append(line[1:].strip())  # Strip '+' and surrounding whitespace
    return additions

def collect_additions(file_path, commits):
    """Collect all additions from given commits for a file."""
    all_additions = []
    for commit in reversed(commits):  # oldest to newest
        additions = get_commit_diff(commit, file_path)
        all_additions.extend(additions)
    return all_additions

def write_additions_to_jsonl(output_path, additions):
    """Write additions to a .jsonl file."""
    with open(output_path, 'w', encoding="utf-8") as file:
        for addition in additions:
            json.dump({"addition": addition}, file)
            file.write("\n")

def get_commit_diff_count(file_path, scrape_meta_path):
    """Return how many commits behind we are and all commits."""
    commits = get_all_commit_hashes(file_path)
    last_scraped = get_last_scraped_commit(scrape_meta_path)

    if not last_scraped or last_scraped not in commits:
        return len(commits), commits

    idx = commits.index(last_scraped)
    return idx, commits

def process_new_commits(file_path, additions_output_path, scrape_meta_path,folder):
    """Main routine to collect new additions and update tracking."""
    pull_latest(folder)
    diff_count, commits = get_commit_diff_count(file_path, scrape_meta_path)
    
    if diff_count == 0:
        print("No new commits to process.")
        return

    new_commits = commits[:diff_count]
    print(f"Processing {diff_count} new commits...")

    additions = collect_additions(file_path, new_commits)
    write_additions_to_jsonl(additions_output_path, additions)
    update_scraped_commit(scrape_meta_path, new_commits[0])
    print(f"Additions written to {additions_output_path} and commit tracker updated.")