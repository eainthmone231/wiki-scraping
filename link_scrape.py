import requests
from bs4 import BeautifulSoup
import json
import argparse
import os 

source = "https://my.wikipedia.org"
dir = os.getcwd()
def link_scrape(url,filename):
    response = requests.get(url)
    encoding = response.encoding if 'charset' in response.headers.get('content-type', '').lower() else None
    html_content = response.content.decode(encoding, 'replace') if encoding else response.text
    soup = BeautifulSoup(html_content,'html5lib')
    main_content = soup.find('div',attrs = {'class':'mw-content-ltr mw-parser-output'})
    all_link = {}
    all_links = main_content.find_all("a")
    for link in all_links:
        all_link[str(link.get('title')).replace("ဤအပိုင်းကို တည်းဖြတ်ရန် -","")] = source+str(link.get("href"))
   
    with open(filename,"w",encoding='utf-8') as outfile:
        json.dump(all_link,outfile,ensure_ascii=False)
    return all_link


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Link Scraping")
    parser.add_argument("url", type=str,help ='Main url you want to scrape')
    parser.add_argument("filename", type=str,help= "save file name")
    args = parser.parse_args()
    save_file = args.filename+".json"
    all_link = link_scrape(args.url,save_file)
