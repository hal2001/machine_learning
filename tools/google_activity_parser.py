# -*- coding: utf-8 -*-
"""
Parses "My Activity" from Google, specifically for Google Search

Author: Aaron Penne
"""

import datetime
from bs4 import BeautifulSoup as bs

# Hard coded file names for now
file_in = "MyActivity.html"
file_out = "my_activity_search.txt"

# Open file with correct encoding
# FIXME this takes too long to run and uses 100% CPU
with open(file_in, encoding="utf8") as f:
    soup = bs(f, "html.parser")

all_divs = soup.find_all(class_="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1")

with open("my_activity_search.txt", "w+") as file:
    file.write("Action\tTerm\tTimestamp\n")
    
for i, div in enumerate(all_divs):
    # Print out current loop iteration
    if i % 100 == 0: print(i)
    try:
        # Strip out the 'Visited' or 'Searched for' text
        action = div.contents[0].replace(u'\xa0', u'')
        # Get the URL or search term
        term = div.contents[1].text
        # Put the date and time into something excel understands
        timestamp = datetime.datetime.strptime(div.contents[3], '%b %d, %Y, %I:%M:%S %p').strftime('%m/%d/%Y %I:%M:%S %p')
        
        # Write to file, tab-delimited
        with open("my_activity_search.txt", "a") as file:
            file.write("{0}\t{1}\t{2}\n".format(action, term, timestamp))
    except:
        # FIXME A lot of errors and skipped chunks, particularly 'Searched for hotels...'
        print("Disregarding '{0}'... ".format(action))