

# # Article Scrapping

#Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd

#check is chromedriver is installed
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

#Visit the Quote to Scrape site
url = 'http://quotes.toscrape.com/'
browser.visit(url)

#Parse the HTML
html = browser.html
html_soup = soup(html, 'html.parser')

#Scrape the Title
title = html_soup.find('h2').text
title

# Scrape the top ten tags
tag_box = html_soup.find('div', class_='tags-box')
# tag_box
tags = tag_box.find_all('a', class_='tag')

for tag in tags:
    word = tag.text
    print(word)


url = 'http://quotes.toscrape.com/'
browser.visit(url)
    

for x in range(1,6):
    html = browser.html
    quote_soup = soup(html, 'html.parser')
    quotes = quote_soup.find_all('span', class_='text')
    for quote in quotes:
        print('page', x, '----------')
        print(quote.text)
    browser.links.find_by_partial_text('Next')    


# # Bookstore scrapping practice - module 10.3.3

#practice by scraping the book url
url = 'http://books.toscrape.com/'
browser.visit(url)


html = browser.html
book_soup = soup(html, 'html.parser')
# Scrape the top ten tags
book_list = book_soup.find_all('article', {'class':'product_pod'})    

#for book in book_list:

    #book = book_list.div.a.img["alt"]

    #print(book)



# # Vist the NASA mars News site: Image Scrapping - module 10.3.4

#visit url
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()

#Find the more info button and click
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()

#Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
#Find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get('src')
img_url_rel

#Use the base url to create an absolute url
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# # Facts table scrapping

df = pd.read_html('https://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df

df.to_html()

browser.quit()



