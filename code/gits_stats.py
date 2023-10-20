from collections import defaultdict
import re
import subprocess
from subprocess import PIPE


def get_stats(args):
    try:
        process = subprocess.Popen(["git", "log", "--format=\"author: %an\"", "--numstat"],
                                           stdout=PIPE,
                                           stderr=PIPE)
        stdout, stderr = process.communicate()
        data = stdout.decode()
    except Exception as e:
        print("Failed: "+ str(e))
        return None
    # Initialize a defaultdict to store data for each author
    author_data = defaultdict(lambda: [0, 0, 0, 0])
    # Split data into lines
    lines = data.strip().split("\n")
    # Initialize variables to keep track of the current author
    current_author = None
    # Iterate through lines
    for line in lines:
        if line.strip('"').startswith("author: "):
            current_author = re.sub(r'^author: (.+)$', r'\1', line).strip()
            author_data[current_author][0] += 1
        else:
            if not line:
                continue
            temp = line.split('\t')
            if not re.match(r'^\d+$', temp[0]) or not re.match(r'^\d+$', temp[1]):
                continue
            insertions, deletions= temp[0], temp[1]
            author_data[current_author][1] += 1
            author_data[current_author][2] += int(insertions)
            author_data[current_author][3] += int(deletions)

    # Print the header
    print("Email                           Commits         Files           Insertions      Deletions       Total Lines")
    print("-----                           -------         -----           ----------      ---------       -----------")
    # Iterate through the author data and print the transformed information
    for author, data in author_data.items():
        commits, files, insertions, deletions = data
        total_lines = insertions + deletions
        print(f"{author:<30} {commits:<15} {files:<15} {insertions:<15} {deletions:<15} {total_lines:<15}")