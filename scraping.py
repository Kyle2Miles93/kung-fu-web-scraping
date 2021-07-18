# import Splinter, Beautiful Soup and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


# Scrape Mars News
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now(),
      "hemispheres": mars_hemispheres(browser)
    }

     # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):


    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("div.list_text", wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')

        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()

        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

    return news_title, news_p


### Featured Images

def featured_image(browser):
        
    # Visit URL
    try:
        PREFIX = "https://web.archive.org/web/20181114023740"
        url = f'{PREFIX}/https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)
        article = browser.find_by_tag('article').first['style']
        article_background = article.split("_/")[1].replace('");',"")
        return f'{PREFIX}_if/{article_background}'
    except:
        return 'https://www.nasa.gov/sites/default/files/styles/full_width_feature/public/thumbnails/image/pia22486-main.jpg'

def mars_facts():

    try:
        # use "read_html" to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None

    # Assign columns and set index of DataFrame
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)
    
    # Convert dataframe into HTML
    return df.to_html(classes="table table-striped")
    
def mars_hemispheres(browser):

        # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    images = browser.find_by_css('a.product-item h3')

    for i in range(len(images)):
        hemispheres = {}
        # find each image url with Splinter
        browser.find_by_css('a.product-item h3')[i].click()
        img = browser.links.find_by_text('Sample').first
        img_url = img['href']
        title_link = browser.find_by_css('h2.title')
        title = title_link.text
        hemispheres = {'img_url': img_url, 'title': title}
        hemisphere_image_urls.append(hemispheres)
        browser.back()

    # 4. Return the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls

   


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())