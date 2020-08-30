


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

def scrape_all():
    #Intitiate headless driver for deployment
    browser = Browser("chrome", executable_path="C:\\Users\\chiko\\Mission-to-Mars\\chromedriver.exe",headless=True)
    #executable_path = {'executable_path': 'chromedriver'}
    #browser = Browser('chrome', **executable_path)

    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph, 
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere": hemisphere_image_urls(browser)
    }
    # Stop webdriver and return data
    browser.quit()
    return data


# # NASA Article scrapping
def mars_news(browser):
    #Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=2)

    #Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:

        slide_elem = news_soup.select_one('ul.item_list li.slide')

        slide_elem.find("div", class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p




# # Vist the NASA mars News site: Image Scrapping - module 10.3.4

def featured_image(browser):

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

    # add the try except
    try:

        #Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get('src')
        
    except AttributeError:
        return None

    #Use the base url to create an absolute url
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url




    # # Facts table scrapping
def mars_facts():
        # Add try/except for error handling
        try:
            ## Use 'read_html' to scrape the facts table into a dataframe
            df = pd.read_html('https://space-facts.com/mars/')[0]
        except BaseException:
            return None

        # Assign columns and set index of dataframe
        df.columns=['Description', 'Mars']
        df.set_index('Description', inplace=True)

        # Convert dataframe into HTML format, add bootstrap
        return df.to_html(classes="table table-dark")

#hemisphere URL and image title
def hemisphere_image_urls(browser):
        # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    html = browser.html
    img_soup = soup(html, 'html.parser')
    results = img_soup.find_all('div', class_="description")
        
    for result in results:
        
        base_link = "https://astrogeology.usgs.gov"
        
        try:   
            links = base_link+result.a['href']
            
            browser.visit(links)
            
            html = browser.html
            img_soup = soup(html, 'html.parser')    
            
            for link in links:
                
                hemispheres = {}
                img_url = img_soup.find('div', class_="downloads").a['href']  
                title = img_soup.find('h2').text
                hemispheres = {'img_url': img_url, 'title': title, }
                    
            hemisphere_image_urls.append(hemispheres)

        except AttributeError as e:
            return None

    # 4. Print the list that holds the dictionary of each image url and title.

    return hemisphere_image_urls

    # 5. Quit the browser
    browser.quit()

if __name__ == "__main__":
    #if running as script, print scraped data
    print(scrape_all())



