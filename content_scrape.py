import requests
from bs4 import BeautifulSoup
import json
import argparse

#interesting content tag only     
def is_interesting(tag):
    return tag.name in ['p', 'ol','ul']

# get elements class to remove and reupdate the main content
def remove_elements(soup, elements_to_remove):
    for tag, attrs in elements_to_remove:
       elements = soup.find_all(tag, attrs=attrs)
       for element in elements:
          element.decompose()
          
# remove unwanted class ul under 'reference list'
def remove_adjacent_ul_under_class(soup, class_name):
    main_elements = soup.find_all(class_=class_name)
    for main_element in main_elements:
        # Find all children of the main element
        children = main_element.find_all_next('ul')

        # Remove all children
        for child in children:
            child.decompose()

def content_scrape(url,save_file):
    print("geeting from outer file" + url)
    response = requests.get(url)
    encoding = response.encoding if 'charset' in response.headers.get('content-type', '').lower() else None
    html_content = response.content.decode(encoding, 'replace') if encoding else response.text
    soup = BeautifulSoup(html_content,'html5lib')
    main_content = soup.find('div',attrs = {'class':'mw-content-ltr mw-parser-output'})

    elements_to_remove = [
        ('div', {'class': 'mw-references-wrap'}),
        ('ul', {'class': 'gallery'}),
        ('div',{'class': 'navbox'}),
        ('div', {'class': 'catlinks'})
    ]
    
    remove_adjacent_ul_under_class(main_content, 'reflist') 
    remove_elements(main_content, elements_to_remove)

    interesting_tags = main_content.find_all(is_interesting)

    # Process the tags in order
    for tag in interesting_tags:
        # Do something with the tag
        with open(save_file, "a" ,encoding='utf-8') as txt_file:
            if tag.name == "p":
                txt_file.write(tag.text)
                #txt_file.write('\n')
            else:
                for li in tag.find_all("li"): 
                    txt_file.write(li.text)
                    txt_file.write('\n')
    txt_file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Content Scraping")
    parser.add_argument("url", type=str,help ='Content url you want to scrape')
    parser.add_argument("filename", type=str,help= "save file name")
    args = parser.parse_args()
    save_file = args.filename+".txt"
    content_scrape(args.url,save_file)



