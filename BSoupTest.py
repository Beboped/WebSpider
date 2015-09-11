# -*- coding: utf-8 -*-
"""
Beautiful Soup based web site tester

Created on Fri Sep 11 08:48:23 2015

@author: Thor
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup, SoupStrainer
import re
from urllib.error import HTTPError

def get_links(url):
    """Takes a url and returns a set with all the links present on the page"""
    html = urlopen(url)
    if html is None:
        raise HTTPError("No Response From Server")
    bsObj = BeautifulSoup(html, "html.parser", parse_only=SoupStrainer("a"))
    return bsObj.findAll("a", {"href":re.compile("^http:\/\/[a-zA-Z]{0,4}\.?datasciencedojo\.com[^.]+(?!\.)")})

urls_encountered = {"http://www.datasciencedojo.com"}
urls_checked = set()
error_list = []
ii = 0
while len(urls_encountered) > 0:
    ii += 1
    if ii > 200:
        break
    else:
        nexturl = urls_encountered.pop()    
        print(nexturl)
    try:
        new_links = get_links(nexturl)
    except HTTPError as e:
        error_list.append((nexturl, e))
    else:
        for tag in new_links:
            if tag['href'] not in urls_checked:
                urls_encountered.add(tag['href'])
    urls_checked.add(nexturl)

print(error_list)
print(urls_checked)