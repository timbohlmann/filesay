import csv
import fnmatch
import os
import sys

ban_reason = input("Reason for the ban: ")

result = ""
for file in os.listdir('.'):
    if fnmatch.fnmatch(file, 'followerlist*.csv'):
        result = file
        break
if(result == ""):
    print("No csv file found!")
    sys.exit()

with open(result, 'r') as csv_file, open("./filesay.txt", 'w') as filesay:
    csv_reader = csv.reader(csv_file, delimiter=','); 
    line_index = 0; 
    for row in csv_reader:
        if line_index > 0:
            filesay.write('/ban {username} {reason}\n'.format(username = row[0], reason = ban_reason))
        
        line_index = line_index + 1
    print("Created filesay textfile.")