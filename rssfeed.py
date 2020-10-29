#Let's create a little rss feed generator in Derrick's favorite language.
#written by kbturk @ 10/28/2020

import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = 'https://usethe.computer'

def error_log(s):
    with open("error_log.txt","w") as f:
        f.write(s)
        f.close()  
        
'''
I. Info scraped from the website boiled down to a list of:

POST TITLE, POST LINK, POST DATE, POST DESCRPTION 

This will return NONE if nothing is found for one of these entries.
'''

#Let's do a little web scraping. returns a urllib3.response.HTTPResponse object.
r = requests.get(URL + "/posts.html", stream=True)
r.encoding = 'utf-8'

#Translate that shit to beautiful soup.
soup = BeautifulSoup(r.text, 'html.parser')

#find the blogpost entries:
entries = soup.find_all("div", class_="linkcerpt")

title,link,date,description = [],[],[],[]

for entry in entries:
    title.append(entry.a.get_text().strip('  \n'))
    link.append(URL + entry.a.get('href'))
    
    #Because I love my husband, I converted dates for him...
    try:
        date.append( datetime.strptime( entry.h4.get_text(), "%Y-%m-%d" ).strftime("%a, %d %b %Y 12:00:00 CST") )
    except ValueError:
        print("issues parsing date. Check that %Y-%m-%d format is used and the date is inside a h4 bracket inside of linkcerpt.")
        
    description.append(entry.p.get_text())

#a little error handling is all I need...
if len(title) != len(link) != len(date) != len(description):
    print("scraper had issues: title, link, and date lengths not equal.")
    error_log(f'title lenghts: {len(title)},\ntitles:\n{title}\n\nlink lengths:{len(link)}\nlinks:\n{link}\n\ndate lengths: {len(date)}\ndates:\n{date}\n\ndescriptions:\n{len(description)}\n{description}')

else:
    print("scraper successfully scraped name, url, date and description from website.")


'''
II. XML Document outline:
    header (xml_doc_header)
        repeated item structure generated from scraped website.
    closure
'''

xml_doc_header = '''<?xml version = "1.0" encoding = "UTF-8" ?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">

<channel>
<atom:link href="https://usethe.computer/rss_feed.xml" rel="self" type="application/rss+xml" />
    <title>use the computer - a blog by Derrick Turk</title>
    <link>https://usethe.computer</link>
    <description></description>'''


''' III. XML Item Structure:
    <item>
        <title>[POST TITLE]</title>
        <pubDate>[POST DATE]</pubDate>
        <link>[POST LINK]</link>
        <description>[POST DESCRIPTION]</description>
    </item>
    ...
</channel>
</rss>'''

a = ["\n<item>\n        <title>","</title>\n        <link>","</link>\n        <pubDate>","</pubDate>\n      <description>","</description>\n<guid>","</guid>\n    </item>"]

xml_body = []

for i in range(len(title)):
    xml_body.append(a[0]+title[i]+a[1]+link[i]+a[2]+date[i]+a[3]+description[i]+a[4]+link[i]+a[5])
xml_body = "".join(xml_body)


xml_doc_closure = '''</channel>\n</rss>'''

xml_doc = "".join([xml_doc_header, xml_body, xml_doc_closure])

#And at the end, we ask ourselves if it was worth it. It probably wasn't.
with open( 'rss.xml','w', encoding = 'utf8' ) as f:
    f.write(xml_doc)
    f.close()