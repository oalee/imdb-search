# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import bs4
import requests
import imdb


def find_ttl_by_name(name):
    url = "http://m.imdb.com/find?ref_=nv_sr_fn&s=tt&q=" + name
    page = requests.get(url)
    
    link = ""
    soup = bs4.BeautifulSoup(page.content,"lxml")
    ttl = ""
    j = 0
    for s in soup.findAll('div'):
        if s.get('class') != None and s.get('class')[0] == 'title':
            ttl = s.contents[1].get('href')    
            break
        
    return ttl
    

ttl = find_ttl_by_name("Toy Story 1".replace(" " , "+"))
if len(ttl) > 0:
    res = imdb.find_detail_by_id(ttl.split("/")[2])
    print(res)