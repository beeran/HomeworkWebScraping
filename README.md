# HomeworkWebScraping

Please download the chromedriver.exe from my github if you do not have a local copy.
My code runs directly on windows. If you are using a mac, you may try with the mac option in scrape_mars.py, but I'm not sure how it works on mac.

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=True)
    #You may want to uncomment and try if you are using a Mac. My program works for Windoes, please make sure you download the chromedriver.exe from my github.
    #/usr/local/bin/chromedriver
    #executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    #return Browser('chrome', **executable_path, headless=False)
