#!/usr/bin/env python3
# file : download.py

import cfscrape
import requests
import comicV2, getReadComicLists, downloadComic
import argparse, json, os

base_url = "http://readcomiconline.to/Comic"

#Scraper instance
scraper = getReadComicLists.create_scraper_new(requests)

#For parsing arguments
parser = argparse.ArgumentParser()

parser.add_argument("-chl", "--chapterlink", dest="chapter_link", default="", help="Chapter Link")
parser.add_argument("-cl", "--comiclink", dest="comic_link", default="", help="comic Link")
parser.add_argument("-c", "--comic", dest="comic_name", default="", help="comic Name")
parser.add_argument("-a", "--all", dest="all", nargs='?', const=True, help="Use -a or --all to download all chapters", type=bool)
parser.add_argument("-d", "--dir", dest="directory", default="Comics", help="Use -d path to change download path default is ./Comics")
parser.add_argument("-s", "--start", dest="start", default=0,help="Use -s chapter.no to start from chapter.no")
parser.add_argument("-e", "--end", dest="end", help="Use -e chapter.no to end at chapter.no")
parser.add_argument("-l", "--list", dest="list_chapters", nargs='?', const=True, help="Lists chapter names", type=bool)

args = parser.parse_args()

comic_link = args.comic_link
comic_name = args.comic_name
chapter_link = args.chapter_link
download_all = args.all
outdir = args.directory

if args.comic_name:
    comic_link = base_url + args.comic_name

if args.comic_link:
    comic_name = comic_link.split("/")[-1]

if args.chapter_link:
    comic_link = "/".join(chapter_link.split("/")[:5])
    comic_name = comic_link.split("/")[-1]

if args.list_chapters and comic_link:

    print("Wait for 10 secs to bypass cloudflare ddos protection ...")
    print("Listing all chapter names of " + comic_link)

    list_chapters, json_data = getReadComicLists.getchcom(comic_link, scraper)

    for chapter in json_data:
        print(chapter['chapter'])

outdir = os.path.join(outdir, comic_name)

if download_all:

    #All chapters
    #Usage -ml "URL" -a True
    #OR -m "Name of comic" -a True
    print("Wait for 10 secs to bypass cloudflare ddos protection ...")
    print("Downloading all chapters from " + comic_link + " ...")

    list_chapters, json_data = getReadComicLists.getchcom(comic_link, scraper)

    #Make a chapters.json file
    downloadComic.write_json(json_data, outdir, 'chapters')

    downloadComic.download_chapters(json_data, outdir, scraper)

elif comic_link and not chapter_link:
    print("It currently supports downloading all chapters or only one chapter")
    print("Use -cl <chapter_URL> to give a chapterlink and download that chapter")
    print("Or -a to download every chapter")

elif chapter_link:

    #Single chapter
    #Usage -cl "" only
    print("Wait for 10 secs to bypass cloudflare ddos protection ...")
    print("Downloading only this chapter " + chapter_link + " ...")

    dec_imgs_list = comicV2.get_img_urls(chapter_link, scraper)

    details = comicV2.get_chapter_detalis(chapter_link, scraper)

    downloadComic.write_json(
            dec_imgs_list,
            os.path.join(outdir, details['title']),
            details['title'] + "_images"
        )

    downloadComic.download_images_and_create_pdf(
            dec_imgs_list,
            os.path.join(outdir, details['title']),
            details['title']
        )