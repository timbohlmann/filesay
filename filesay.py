import csv
import fnmatch
import os
import sys
import requests
from dotenv import load_dotenv
import tkinter

load_dotenv()
DEV_KEY = os.getenv("DEV_KEY")

ban_reason = "" # input("Reason for the ban: ")
csv_path = ""
result = ""

# Find the csv file
for file in os.listdir('.'):
    if fnmatch.fnmatch(file, 'followerlist*.csv'):
        csv_path = file
        break
if csv_path == "":
    print("No csv file found!")
    sys.exit()


# Extract usernames from csv
with open(csv_path, 'r') as csv_file:  # , open("./filesay.txt", 'w') as filesay:
    csv_reader = csv.reader(csv_file, delimiter=','); 
    line_index = 0; 
    for row in csv_reader:
        if line_index > 0:
            # filesay.write('/ban {username} {reason}\n'.format(username = row[0], reason = ban_reason))
            result = result + '/ban {username} {reason}\n'.format(username=row[0], reason=ban_reason)
        line_index = line_index + 1

# Create pastebin
url = "https://pastebin.com/api/api_post.php"
values = {
    'api_dev_key': DEV_KEY,
    "api_option": "paste",
    "api_paste_code": result,
    "api_paste_expire_date": "1D"
}

response = requests.post(url, values)


print(response.text)
