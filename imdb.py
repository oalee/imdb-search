#!/usr/bin/env python

import sys
import requests
import lxml.html
import bs4

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

def find_move_by_name(name):
    ttl = find_ttl_by_name(name.replace(" " ,"+"))
    if len(ttl) > 0:
        ttl = ttl.split("/")[2]
        return find_detail_by_id(ttl)

def find_detail_by_id(id):
    hxs = lxml.html.document_fromstring(requests.get("http://imdb.com/title/" + id).content)
    movie = {}
    try:
        movie['title'] = hxs.xpath('//h1')[0].text_content().split("\xa0")[0]
    except IndexError:
        movie['title'] =""
    try:
        movie['year'] = hxs.xpath('//h1')[0].text_content().split("\xa0")[1].replace(" ","").replace("(","").replace(")","")
    except IndexError:
        pass

    try:
        movie['genre'] =[i.text_content() for i in hxs.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "subtext", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "itemprop", " " ))]')]
    except IndexError:
        movie['genre'] = []
    try:
        movie['rating'] = hxs.xpath('//strong//span')[0].text_content()
    except IndexError:
        movie['rating'] = ""
    try:
        movie['storyline'] = hxs.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "summary_text", " " ))]')[0].text_content().replace("                    ","").replace("            ","")
    except IndexError:
        movie['storyline'] = ""
    try:
        movie['metascore'] = hxs.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "titleReviewBarSubItem", " " ))]//span')[0].text_content()
    except IndexError:
        movie['metascore'] = 0

    return movie

'''
    try:
        movie['release_date'] = hxs.xpath('//*[@id="overview-top"]/div[2]/span[3]/a/text()')[0].strip()
    except IndexError:
        try:
            movie['release_date'] = hxs.xpath('//*[@id="overview-top"]/div[2]/span[4]/a/text()')[0].strip()
        except Exception:
            movie['release_date'] = ""

    try:
        movie['description'] = hxs.xpath('//*[@id="overview-top"]/p[2]/text()')[0].strip()
    except IndexError:
        movie['description'] = ""
    try:
        movie['director'] = hxs.xpath('//*[@id="overview-top"]/div[4]/a/span/text()')[0].strip()
    except IndexError:
        movie['director'] = ""
    try:
        movie['stars'] = hxs.xpath('//*[@id="overview-top"]/div[6]/a/span/text()')
    except IndexError:
        movie['stars'] = ""
    try:
        movie['poster'] = hxs.xpath('//*[@id="img_primary"]/div/a/img/@src')[0]
    except IndexError:
        movie['poster'] = ""
    try:
        movie['gallery'] = hxs.xpath('//*[@id="combined-photos"]/div/a/img/@src')
    except IndexError:
        movie['gallery'] = ""

    try:
        movie['votes'] = hxs.xpath('//*[@id="overview-top"]/div[3]/div[3]/a[1]/span/text()')[0].strip()
    except IndexError:
        movie['votes'] = ""
'''
