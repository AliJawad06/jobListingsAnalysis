import subprocess
import re
import json

def get_last_10_commits(file_path):
    """Get the last 10 commit hashes for a specific file."""
    result = subprocess.run(["git", "log", "--format=%H", "-n", "10", "--", file_path],
                            capture_output=True, text=True, check=True)
    return result.stdout.strip().split("\n")

def get_commit_diff(commit_hash, file_path):
    """Get the diff for a specific commit and extract added lines."""
    result = subprocess.run(["git", "show", commit_hash, "--", file_path],
                            capture_output=True, text=True, check=True)
    
    diff_lines = result.stdout.split("\n")
    additions = [line[1:] for line in diff_lines if line.startswith("+") and not line.startswith("+++")]
    
    return additions

def collect_additions(file_path):
    """Collect all additions from the last 10 commits for a file."""
    commits = get_last_10_commits(file_path)
    all_additions = []
    
    for commit in reversed(commits):  # Process from oldest to newest
        additions = get_commit_diff(commit, file_path)
        all_additions.extend(additions)
    
    return all_additions

def write_additions_to_jsonl(file_path, additions):
    """Write additions to a .jsonl file, each addition in its own line."""
    with open(file_path, 'w') as file:
        for addition in additions:
            json.dump({"addition": addition}, file)  # Write each addition as a JSON object
            file.write("\n") 

# Example usage
#file_path = "README.md"  # Change this to your file path
#additions = collect_additions(file_path)


#jsonl_file_path = "additions.jsonl"  # Output file name
#write_additions_to_jsonl(jsonl_file_path, additions)

#print("\n".join(additions))  # Print all collected additions
