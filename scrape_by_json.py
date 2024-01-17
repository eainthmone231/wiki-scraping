import requests
from bs4 import BeautifulSoup
import json
import argparse
import os
from link_scrape import link_scrape
from content_scrape import content_scrape 

def scrapper_pipeline(jsonfile):
    with open(jsonfile,encoding="utf-8") as f_in:
        res = json.load(f_in)
        print(res)
        for key,value in res.items():
            content_scrape(value,key+".txt")
    
if __name__ == '__main__':
    scrapper_pipeline("mandalay_link.json")