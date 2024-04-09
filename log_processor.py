#!/usr/bin/env python3

import re
import sys
import socket
from collections import defaultdict
from alive_progress import alive_bar

# Initialize total bytes to 0
total_bytes = 0

# Dictionaries to store counts of each category
data = {
    'hosts': defaultdict(int),
    'domains': defaultdict(int),
    'dates': defaultdict(int),
    'hours': defaultdict(int),
    'stat': defaultdict(int),
    'methods': defaultdict(int),
    'http_versions': defaultdict(int),
    'urls': defaultdict(int),
    'browser': defaultdict(int),
    'browser_family': defaultdict(int),
    'referer': defaultdict(int),
    'referer_domain': defaultdict(int),
    'os': defaultdict(int)
}


# Function to perform reverse IP lookups
def get_hostname(ip_address):
    try:
        hostname = socket.gethostbyaddr(ip_address)[0]
        return hostname
    except socket.herror:
        return ip_address


def generate_report(title, data_dict, logfiles):
    total_count = sum(data_dict['hosts'].values())
    with open('cmisbach.summary', 'w') as file:
        file.write(f"{title}\n\n")
        file.write(f"Logfile(s) processed: {', '.join(logfiles)}\n\n")
        file.write("==============================================================================\n")
        file.write("Hostnames Report\n")
        file.write("==============================================================================\n\n")
        file.write("Count  Percent  Resource\n")
        file.write("-----  -------  --------\n")

        # Sort hostnames alphabetically before iterating
        for host in sorted(data_dict['hosts'].keys(), key=lambda s: s.lower()):
            count = data_dict['hosts'][host]
            percent = (count / total_count) * 100
            file.write(f"{count:5} {percent:7.2f}%  {host}\n")

        file.write("\n==============================================================================\n")
        file.write("Domains Report\n")
        file.write("==============================================================================\n\n")
        file.write("Count  Percent  Resource\n")
        file.write("-----  -------  --------\n")

        # Print "DOTTED QUAD OR OTHER" first
        if "DOTTED QUAD OR OTHER" in data_dict['domains']:
            count = data_dict['domains']["DOTTED QUAD OR OTHER"]
            percent = (count / total_count) * 100
            file.write(f"{count:5} {percent:7.2f}%  DOTTED QUAD OR OTHER\n")

        # Print the rest of the domains sorted
        for domain in sorted([d for d in data_dict['domains'].keys() if d != "DOTTED QUAD OR OTHER"],
                             key=lambda s: s.lower()):
            count = data_dict['domains'][domain]
            percent = (count / total_count) * 100
            file.write(f"{count:5} {percent:7.2f}%  {domain}\n")

        file.write("\n==============================================================================\n")
        file.write("Dates Report\n")
        file.write("==============================================================================\n\n")
        file.write("Count  Percent  Resource\n")
        file.write("-----  -------  --------\n")

        for date in data_dict['dates']:
            count = data_dict['dates'][date]
            percent = (count / total_count) * 100
            file.write(f"{count:5} {percent:7.2f}%  {date}\n")

        file.write("\n==============================================================================\n")
        file.write("Hours Report\n")
        file.write("==============================================================================\n\n")
        file.write("Count  Percent  Resource\n")
        file.write("-----  -------  --------\n")

        for hours in data_dict['hours']:
            count = data_dict['hours'][hours]
            percent = (count / total_count) * 100
            file.write(f"{count:5} {percent:7.2f}%  {hours}\n")

        file.write("\n==============================================================================\n")
        file.write("Status Code Report\n")
        file.write("==============================================================================\n\n")
        file.write("Count  Percent  Resource\n")
        file.write("-----  -------  --------\n")

        for stat in data_dict['stat']:
            count = data_dict['stat'][stat]
            percent = (count / total_count) * 100
            file.write(f"{count:5} {percent:7.2f}%  {stat}\n")

        file.write("\n==============================================================================\n")
        file.write("Method Report\n")
        file.write("==============================================================================\n\n")
        file.write("Count  Percent  Resource\n")
        file.write("-----  -------  --------\n")

        for method in data_dict['methods']:
            count = data_dict['methods'][method]
            percent = (count / total_count) * 100
            file.write(f"{count:5} {percent:7.2f}%  {method}\n")

        file.write("\n==============================================================================\n")
        file.write("HTTP Version Report\n")
        file.write("==============================================================================\n\n")
        file.write("Count  Percent  Resource\n")
        file.write("-----  -------  --------\n")

        for http_version in data_dict['http_versions']:
            count = data_dict['http_versions'][http_version]
            percent = (count / total_count) * 100
            file.write(f"{count:5} {percent:7.2f}%  {http_version}\n")

        file.write("\n==============================================================================\n")
        file.write("Resource Report\n")
        file.write("==============================================================================\n\n")
        file.write("Count  Percent  Resource\n")
        file.write("-----  -------  --------\n")

        for resource in data_dict['urls']:
            count = data_dict['urls'][resource]
            percent = (count / total_count) * 100
            file.write(f"{count:5} {percent:7.2f}%  {resource}\n")

        file.write("\n==============================================================================\n")
        file.write("Browser Report\n")
        file.write("==============================================================================\n\n")
        file.write("Count  Percent  Resource\n")
        file.write("-----  -------  --------\n")

        for browser in data_dict['browser']:
            count = data_dict['browser'][browser]
            percent = (count / total_count) * 100
            file.write(f"{count:5} {percent:7.2f}%  {browser}\n")

        file.write("\n==============================================================================\n")
        file.write("Browser Family Report\n")
        file.write("==============================================================================\n\n")
        file.write("Count  Percent  Resource\n")
        file.write("-----  -------  --------\n")

        for browser_family in data_dict['browser_family']:
            count = data_dict['browser_family'][browser_family]
            percent = (count / total_count) * 100
            file.write(f"{count:5} {percent:7.2f}%  {browser_family}\n")

        file.write("\n==============================================================================\n")
        file.write("Referer Report\n")
        file.write("==============================================================================\n\n")
        file.write("Count  Percent  Resource\n")
        file.write("-----  -------  --------\n")

        for referer in data_dict['referer']:
            count = data_dict['referer'][referer]
            percent = (count / total_count) * 100
            file.write(f"{count:5} {percent:7.2f}%  {referer}\n")

        file.write("\n==============================================================================\n")
        file.write("Referer Domains Report\n")
        file.write("==============================================================================\n\n")
        file.write("Count  Percent  Resource\n")
        file.write("-----  -------  --------\n")

        for referer_domain in data_dict['referer_domain']:
            count = data_dict['referer_domain'][referer_domain]
            percent = (count / total_count) * 100
            file.write(f"{count:5} {percent:7.2f}%  {referer_domain}\n")

        file.write("\n==============================================================================\n")
        file.write("Operating Systems Report\n")
        file.write("==============================================================================\n\n")
        file.write("Count  Percent  Resource\n")
        file.write("-----  -------  --------\n")

        for os in data_dict['os']:
            count = data_dict['os'][os]
            percent = (count / total_count) * 100
            file.write(f"{count:5} {percent:7.2f}%  {os}\n")

        file.write(f'\nTotal bytes served: {total_bytes}')


def main():
    global total_bytes
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <logfile1> <logfile2> ... <logfileN>")
        sys.exit(1)

    for logfile in sys.argv[1:]:
        with open(logfile, 'r') as file:
            total_lines = sum(1 for line in file)
            file.seek(0)  # Reset file pointer to the beginning after counting lines
            with alive_bar(total_lines, title=f'Processing log {logfile}') as bar:
                for line in file:
                    bar()
                    # Search for ip addresses
                    host_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                    # If there is a match enter if statement
                    if host_match:
                        host_ip = host_match.group(1)
                        data['hosts'][get_hostname(host_ip)] += 1
                        # Find the hostname using the function provided
                        host_name = get_hostname(host_ip)
                        # Check the hostnames for a domain
                        domain_match = re.search(r'\b\w+\.(com|net)\b', host_name)
                        # If domain, find and add to domain dictionary
                        if domain_match:
                            domain = domain_match.group(0)
                            data['domains'][domain] += 1
                        else:
                            data['domains']['DOTTED QUAD OR OTHER'] += 1

                    # Search log file for dates
                    dates_match = re.search(r'\[(\d+/\w+/\d+)', line)
                    # If there is a match capture and add to dictionary
                    if dates_match:
                        date = dates_match.group(1)
                        data['dates'][date] += 1

                    # Search log file for hours - right after date
                    hours_match = re.search(r'\[(\d+/\w+/\d+):(\d+)', line)
                    # If matched, capture and add to dict
                    if hours_match:
                        hours = hours_match.group(2)
                        data['hours'][hours] += 1

                    # Searching log file for stat and bytes
                    stat_bytes_match = re.search(r'\s(\d+).(\d+)\s', line)
                    if stat_bytes_match:
                        stat = stat_bytes_match.group(1)
                        bytes = stat_bytes_match.group(2)
                        data['stat'][stat] += 1
                        total_bytes += int(bytes)

                    method_http_resource = re.search(r'"(\w+) (\S+) (\S+)"', line)
                    if method_http_resource:
                        method = method_http_resource.group(1)
                        url = method_http_resource.group(2)
                        http_version = method_http_resource.group(3)
                        data['methods'][method] += 1
                        data['http_versions'][http_version] += 1
                        data['urls'][url] += 1

                    # Extract the user-agent string
                    user_agent_match = re.search(r'" "([^"]+)"$', line)
                    if user_agent_match:
                        user_agent = user_agent_match.group(1)
                        data['browser'][user_agent] += 1

                        # Classify browser family
                        if "Chrome" in user_agent:
                            data['browser_family']['Chrome'] += 1
                        elif "Firefox" in user_agent:
                            data['browser_family']['Firefox'] += 1
                        elif "MSIE" in user_agent or "Edge" in user_agent or "Trident" in user_agent:
                            data['browser_family']['Microsoft'] += 1
                        elif "Safari" in user_agent and not "Chrome" in user_agent:
                            data['browser_family']['Safari'] += 1
                        else:
                            data['browser_family']['Other'] += 1

                    # Extract the referer URL
                    referer_match = re.search(r' "([^"]+)" "', line)
                    if referer_match:
                        referer = referer_match.group(1)
                        data['referer'][referer] += 1

                        # Extract referer domain
                        referer_domain_match = re.search(r'http[s]?://([^/]+)', referer)
                        if referer_domain_match:
                            referer_domain_full = referer_domain_match.group(1)
                            # Extract the TLD and SLD only
                            tld_sld_match = re.search(r'([a-zA-Z0-9-]+\.[a-zA-Z0-9]+)$', referer_domain_full)
                            if tld_sld_match:
                                referer_domain = tld_sld_match.group(1)
                                data['referer_domain'][referer_domain] += 1
                            else:
                                data['referer_domain']['NONE'] += 1
                        else:
                            data['referer_domain']['NONE'] += 1

                    # Example: classify operating system (you would need a more comprehensive method)
                    if "Windows" in user_agent:
                        data['os']['Windows'] += 1
                    elif "Linux" in user_agent:
                        data['os']['Linux'] += 1
                    else:
                        data['os']['Other'] += 1

            generate_report("Apache Logfile Processor", data, sys.argv[1:])


# Run the script
if __name__ == "__main__":
    main()
