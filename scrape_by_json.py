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
        for key,value in res.items():
            try:
                response = requests.get(value)
                if response.status_code == 200:
                    content_type = response.headers.get('Content-Type')
                    if content_type and 'text/html' in content_type:
                        content_scrape(value,key+".txt")
                        print(f"{key}: Valid HTML link - {value}")
                    else:
                        print(f"{key}: Not a valid HTML link - {value}")
            except:
                print(f"{key}: Error accessing link - {value}")
           
    
if __name__ == '__main__':
    scrapper_pipeline("magway.json")