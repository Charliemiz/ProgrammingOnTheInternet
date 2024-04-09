#!/usr/bin/env python3

import subprocess
import re
import sys

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} account")
    sys.exit(1)

account = sys.argv[1]
if len(account) > 8:
    account = account[:8]

# Run 'last' command and get the output
raw_results = subprocess.run(['last'], stdout=subprocess.PIPE)
results_str = raw_results.stdout.decode('utf-8')

# Improved Regular Expression pattern
pattern = re.compile(
    r"(" + re.escape(account) + r"\w*)\s+(pts/\d+)\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+"
    r"([A-Za-z]{3}\s+[A-Za-z]{3}\s+\d+)\s+(\d{2}:\d{2})\s+"
    r"(-\s+\d{2}:\d{2}\s+\((\d{2}:\d{2})\)|still logged in)"
)

matches = pattern.findall(results_str)

total_logins = len(matches)
hours = 0
minutes = 0

print(f"Here is a summary of the logins for {account}:\n")

for num, match in enumerate(matches, start=1):
    user, terminal, ip, date, login_time, _, duration = match
    duration = duration if duration else "still logged in"
    print(f"{num}. {user} {terminal} {ip} {date} {login_time} {duration}")
    
    # Calculate total hours and minutes
    if duration != "still logged in":
        h, m = [int(x) for x in duration.split(":")]
        hours += h
        minutes += m

# Convert total minutes to hours:minutes format
hours += minutes // 60
minutes = minutes % 60

print(f"\nAccount: {account}")
print(f"Total logins: {total_logins}")
print(f"{hours:02} hours and {minutes:02} minutes")
