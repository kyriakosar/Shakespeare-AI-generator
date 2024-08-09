import sys
import os
from lxml import html
import requests
from bs4 import BeautifulSoup
import json

poemhunter_url = 'https://www.poemhunter.com'
poetrydb_url = 'https://poetrydb.org'
# topic, artist = 'joy', None     # Shakespeare
topic, artist = None, 'Shakespeare'    

def retrieve_poems_topic(topic):
    # connect to the website
    try:
        html_text = requests.get(f'{poemhunter_url}/poems/{topic}/').text
    except:
        print(f'Error: Unable to connect to the website')
        sys.exit()
    soup = BeautifulSoup(html_text, 'html.parser')

    # get all the links to the poems
    poems_links = []
    for link in soup.find_all('a'):
        poems_links.append(link.get('href'))
    poems_links = list(set(poems_links))
    print(f'Number of available links: {len(poems_links)}')
    print(f'Stored the following links: {poems_links}')

    # find poems links that are direct links to poems
    direct_poem_links = []
    count = 0
    for poem_link in poems_links:
        if poem_link == None:
            continue
        tokens = poem_link.split('/')
        if tokens[1] == 'poem':
            count += 1 
            direct_poem_links.append(poem_link)

    f = open(f'scraper_results_{topic}.txt', 'w', encoding="utf-8")
    for link in direct_poem_links:
        try:
            html_text = requests.get(f'{poemhunter_url}{link}')
        except:
            print(f'Error: Unable to connect to the website')
            sys.exit()

        dom = html.fromstring(html_text.content)
        p = dom.xpath('/html/body/div[1]/div[4]/div[1]/div[1]/div[2]/div[4]')
        if len(p) == 0:
            continue
        f.write(f'{poemhunter_url}{link}')
        f.write(p[0].text_content())
        f.write('\n')
        f.write('-' * 100)
        f.write('\n')
    f.close()


def retrieve_poems_artist(artist):
    # connect to the website
    try:
        html_text = requests.get(f'{poetrydb_url}/author,title/{artist};Sonnet').text
    except:
        print(f'Error: Unable to connect to the website')
        sys.exit()
    soup = BeautifulSoup(html_text, 'html.parser')

    f = open(f'scraper_results_{artist}.txt', 'w', encoding="utf-8")
    f.write(str(soup))
    f.close()


if __name__ == '__main__':
    if artist == None:
        print(f'[Scraper:] Retrieving poems for topic {topic}')
        retrieve_poems_topic(topic)
    else:
        print(f'[Scraper:] Retrieving poems for artist {artist}')
        retrieve_poems_artist(artist)
