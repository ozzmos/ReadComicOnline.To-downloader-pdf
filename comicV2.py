#!/usr/bin/env python3
# file : kissV2.py

import cfscrape #Only py3
import requests
from bs4 import BeautifulSoup as soup
import sys, re, os, ast
import subprocess


def create_scraper_new(requests):
    """
    Returns a new scraper instance
    """
    session = requests.session()
    scraper = cfscrape.create_scraper(sess=session)

    #Important to request the mobile/switchtodesktop page

    print("Getting Info ...")
    print("It might take upto 10 secs ...")
    mainpage = scraper.get("http://readcomiconline.to/Mobile/SwitchToDesktop").content

    return scraper


def scrape_get_scripts(scraper, urls = []):
    """
    Returns script lists from the webpages of all urls given
    
    First url takes 10 seconds and others will be immediate

    scraper is passed because:
    
    The advantage is to use the same cfscrape instance to get all the urls
    It would be useless if we have to wait for 10 secs for every link
    
    """

    scripts = []
    for url in urls:
        print(url)
        html_text = scraper.get(url).content
        souped_html = soup(html_text,"lxml")
        scripts.append(souped_html.findAll("script"))
    return scripts



def get_img_urls_from_scripts(sc_lists):
    """
    Returns encrypted img-link lists from given script lists

    Uses python re module
    """
    
    #I'm accessing the 11th element from scripts list from beautifulsoup
    #Need to think of a better way of accessing

    #ex:
    #Like get only script tags with no src attributes
    # this will slightly decrease the space complexicity
    results = []

    for sc_list in sc_lists:
        script_final = sc_list[15]

        #This gives all the image links like grep
        results.append(re.findall(r'lstImages.push\("(.*)"\);', str(script_final.text)))

    return results


def get_img_urls(chapter_url, scraper):
    """
    Returns list of images of a chapter
    """

    list_scripts = scrape_get_scripts(scraper, urls=[chapter_url])
    enc_lists = get_img_urls_from_scripts(list_scripts)

    return enc_lists[0]

def get_chapter_detalis(chapter_url, scraper):
    """
    Returns chapter details of a particular chapter

    {
        title,
        chapter_no,
        date
    }
    """
    chapter_no = None
    title = ""
    date = ""
    
    comic_link = "/".join(chapter_url.split("/")[:5])
    html_text = scraper.get(comic_link).content
    souped_html = soup(html_text,"lxml")

    print(comic_link, "comic_link")

    table = souped_html.find("table",{"class":"listing"})
    links = table.findAll("tr")


    json_data = []

    index = 1

    for link in links:
        cells = link.findAll("td")
        if not cells:
            continue

        a_tag = cells[0].find("a")

        url_chapter = "http://readcomiconline.to" + a_tag["href"]

        json_data.append({
            "title": re.sub('[^\w\s-]', '', a_tag.get_text().strip().replace(':', " -")),
            "link": url_chapter,
            "date": cells[1].get_text(),
            "pos":index
        })
        index += 1

    for chapter in json_data:
        if chapter['link'] in chapter_url:
            title = chapter['title']
            chapter_no = index - chapter['pos']
            date = chapter['date']

    return {
            "title" : title,
            "chapter_no" : chapter_no,
            "date": date    
    }

if __name__ == "__main__":
    urls = [
        "http://readcomiconline.to/Comic/Ultimate-Spider-Man-2000/Annual-1?id=8271&quality=lq",
        "http://readcomiconline.to/Comic/Ultimate-Spider-Man-2000/Annual-1?id=8271&quality=hq"
        ]

    scraper = create_scraper_new(requests)

    scripts = scrape_get_scripts(scraper, urls=urls)

    print(get_img_urls_from_scripts(sc_lists=scripts))

    details = get_chapter_detalis(urls[0], scraper)

    print(details,"details")

    #All functions working as expected