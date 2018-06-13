#!/usr/bin/env python3
# file : getKissManagList.py

import cfscrape, re
import requests
from bs4 import BeautifulSoup as soup

base_url = "http://readcomiconline.to"

#Initiate just one scraper and use every where

def create_scraper_new(requests):
    """
    Returns a new scraper instance
    """
    session = requests.session()
    scraper = cfscrape.create_scraper(sess=session)


    # This is extremely important in case of this website as it is returning mobile pages when requested
    # To make it send desktop pages we have no choice to make the scraper request for the desktop site at the beggining
    # So this will take 10 secs
    # do getReadComicLists.create_scraper_new() everytime to not have any conflicts regarding mobile pages and desktop pages 
    print("Getting Info ...")
    print("It might take upto 10 secs ...")
    mainpage = scraper.get("http://readcomiconline.to/Mobile/SwitchToDesktop").content

    return scraper

def getchcom(url, scraper):
    """
    Name : get_chapters_of_comic

    Usage: return_value[0] contains the list 

    Returns the chapter links list and a json data for given valid url of the comic

    eg:
        http://readcomiconline.to/Comic/Ultimate-Spider-Man-2000
        
    Use getchchlnk() to get all chapter links from a chapter link
    """

    page = scraper.get(url).content

    souped_html = soup(page, "lxml")

    table = souped_html.find("table",{"class":"listing"})
    links = table.findAll("a")

    ch_links = []

    data_for_json = []

    for link in links:

        url_chapter = base_url + link["href"]
        ch_links.append(url_chapter)

        data_for_json.append({
            "chapter": re.sub('[^\w\s-]', '', link.get_text().strip().replace(':', " -")),
            "link": url_chapter
        })
    
    return (ch_links, data_for_json)

def getchchlnk(ch_url, scraper):
    """
    Name : get_chapter_links_from_a_chapter_link

    Returns the chapter links array for given valid url of some chapter

    eg:
        http://readcomiconline.to/Comic/Ultimate-Spider-Man-2000/Annual-1?id=8271&quality=hq
        http://readcomiconline.to/Comic/Ultimate-Spider-Man-2000/Annual-1?id=8271&quality=lq

    Use getchcom() to get all chapter links of comic
    """

    com_page = "/".join(ch_url.split("/")[:5]) + "/"
    print("url ", com_page)

    return getchcom(com_page, scraper)

if __name__ == "__main__":

    scraper = create_scraper_new(requests)

    url = "http://readcomiconline.to/Comic/Ultimate-Spider-Man-2000/Annual-1?id=8271&quality=lq"

    list_chapters, data = getchchlnk(url, scraper)

    print(data)


# All the functions work