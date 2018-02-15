# -*- coding: utf-8 -*-
"""
Parses "My Activity" from Google, specifically for Google Search

Author: Aaron Penne

Example input of a single Google search:
    <div class="outer-cell mdl-cell mdl-cell--12-col mdl-shadow--2dp">
        <div class="mdl-grid">
            <div class="header-cell mdl-cell mdl-cell--12-col">
                <p class="mdl-typography--title">
                    Search<br>
                </p>
            </div>
            <div class="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1">
                Searched for&nbsp;
                <a href="https://www.google.com/search?q=download+google+my+activity">
                    download google my activity
                </a><br>
                    Feb 12, 2018, 1:23:11 PM
            </div>
            <div class="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1 mdl-typography--text-right">
            </div>
            <div class="content-cell mdl-cell mdl-cell--12-col mdl-typography--caption">
                <b>Products:</b><br>&emsp;Search<br>
            </div>
        </div>
    </div>
    
Example output:
    Searched for    download google my activity    02/12/2018 01:23:11 PM
"""

import datetime
from bs4 import BeautifulSoup

# Hard coded file names for now
my_path = "C:/tmp/"
file_in = my_path + "MyActivity.html"
file_shrunk = my_path + "MyActivity_Shrunk.html"
file_out = my_path + "MyActivity_Clean.txt"

# Create smaller intermediate file to speed up processing
with open(file_in, "r", encoding="utf8") as f_in:
    with open(file_shrunk, "w+", encoding="utf8") as f_out:
        for line in f_in:
            # Replaces large class names with simple ones, cuts file size in half and makes code more readable
            line = line.replace("\"outer-cell mdl-cell mdl-cell--12-col mdl-shadow--2dp\"", "div_A")
            line = line.replace("\"mdl-grid\"", "div_B")
            line = line.replace("\"header-cell mdl-cell mdl-cell--12-col\"", "div_C")
            line = line.replace("\"mdl-typography--title\"", "p_A")
            line = line.replace("\"content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1\"", "div_D")
            line = line.replace("\"content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1 mdl-typography--text-right\"", "div_E")
            line = line.replace("\"content-cell mdl-cell mdl-cell--12-col mdl-typography--caption\"", "div_F")
            # Adds line breaks between main divs
            line = line.replace("</div></div></div><div", "</div></div></div>\n<div")
            f_out.write(line)

# Open file with correct encoding
with open(file_shrunk, encoding="utf8") as f:
    soup = BeautifulSoup(f, "lxml")  # Need to have lxml installed https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser

# Pulls out all div contents which hold the search details
all_divs = soup.find_all(class_="div_D")

with open(file_out, "w+", encoding="utf8") as f:
    # Write headers
    f.write("Action\tTerm\tTimestamp\n")
    for i, div in enumerate(all_divs):
        try:
            # Strip out the 'Visited' or 'Searched for' text
            action = div.contents[0].replace(u'\xa0', u'')
            # Get the URL or search term
            term = div.contents[1].text.replace('\t', ' ')
            # Put the date and time into something excel understands
            timestamp = datetime.datetime.strptime(div.contents[-1], '%b %d, %Y, %I:%M:%S %p').strftime('%m/%d/%Y %I:%M:%S %p')

            # Write to file, tab-delimited
            f.write("{0}\t{1}\t{2}\t{3}\n".format(i, action, term, timestamp))
        except:
            # FIXME A lot of errors and skipped chunks, particularly 'Searched for hotels...'
            print("{0} Disregarding '{1}'... ".format(i, div.text))
