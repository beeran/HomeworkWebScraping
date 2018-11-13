from splinter import Browser
from bs4 import BeautifulSoup
import time
import requests
import pandas as pd 

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=True)
    #You may want to uncomment and try if you are using a Mac. My program works for Windoes, please make sure you download the chromedriver.exe from my github.
    #/usr/local/bin/chromedriver
    #executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    #return Browser('chrome', **executable_path, headless=False)


def try_(fn):
    count = 0
    while True:
        result = fn()
        if result != None: return result
        
        count = count + 1
        if (count > 5):
            raise RuntimeError(f'Exceeded {count} retries')

        # Sleep 100ms
        time.sleep(0.1)

# Returns map like {'news_title': '...', 'news_p': '...'}.
def scrape_news(browser):
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    #Scrape page into Soup:
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    def _find_news():
        return soup.select_one("ul.item_list li.slide")
    
    result = try_(_find_news)
    news_title = result.find("div", class_ = 'content_title').get_text()
    news_p = result.find("div", class_ = "article_teaser_body").get_text()
    return {'news_title': news_title, 'news_p': news_p}

# Returns a String representing image URL.
def scrape_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    #Scrape page into Soup:
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    def _find_image():
        return soup.select_one("div.image_and_description_container div.img img")
    
    result = try_(_find_image)
    return 'https://www.jpl.nasa.gov' + result['src']

def scrape_twtter():
    #TODO: scrape twitter to get weather
    return 'Some Tweets here'

# Returns facts table HTML.
def scrape_facts():
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['description', 'value']
    df.set_index('description', inplace=True)
    return df.to_html()

# Returns a list of map, each map is {'title': '...', 'image_url': '...'}.
def scrape_hemispheres(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    def _find_all_items():
        return soup.find_all('div', class_='item')
    
    results = try_(_find_all_items)
    maps = []
    for result in results:
        title = result.find('h3').get_text().replace(' Enhanced', '')
        img_src = 'https://astrogeology.usgs.gov' + result.find('img')['src']
        maps.append({'title': title, 'image_url': img_src})
    
    return maps

def scrape(): 
    browser = init_browser()
    result = {}
    
    result.update(scrape_news(browser))
    result['featured_image_url'] = scrape_image(browser)
    result['hemispheres'] = scrape_hemispheres(browser)
    result['weather'] = scrape_twtter()
    result['facts_table_html'] = scrape_facts()
    
    # Close the browser after scraping
    browser.quit()
    
    return result

# result = scrape()
# print(result)



