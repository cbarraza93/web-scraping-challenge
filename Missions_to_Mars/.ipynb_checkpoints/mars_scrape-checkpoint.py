from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd
from selenium import webdriver

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

##news
    news_url = 'https://redplanetscience.com/'
    browser.visit(news_url)
    html = browser.html
    soup = bs(html, 'html.parser')

    results = soup.find_all('div', class_='list_text')
    result = results[0]

    todays_date = result.find('div', class_= 'list_date').text
    news_t = result.find('div', class_='content_title').text
    news_p = result.find('div', class_='article_teaser_body').text

##space images
    feat_image_url = 'https://spaceimages-mars.com/'
    browser.visit(feat_image_url)
    html = browser.html
    soup = bs(html, 'html.parser')

    browser.links.find_by_partial_text('FULL IMAGE').click()

    html = browser.html
    soup = bs(html, 'html.parser')

    image_box = soup.find('div', class_='fancybox-inner')
    feat_image_url = feat_image_url.replace('index.html', '') + image_box.img['src']

##facts
    facts_url = 'https://galaxyfacts-mars.com'
    mars_facts = pd.read_html(facts_url,header =0)[0]
    facts_df = pd.DataFrame(mars_facts)
    facts_df = facts_df.reset_index(drop=True)
    facts_df = facts_df.set_index("Mars - Earth Comparison")
    tables = pd.DataFrame.to_html(facts_df)

##hemispheres
    hemis_url = 'https://marshemispheres.com/'
    browser.visit(hemis_url)
    html = browser.html
    soup = bs(html, 'html.parser')

    hemis_img_urls = []
    download_img_urls = []

    results = soup.find("div", class_ = "result-list" )
    hemispheres = results.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end = hemisphere.find("a")["href"]
        image_link = "https://marshemispheres.com/" + end    
        browser.visit(image_link)
        html = browser.html
        soup = bs(html, "html.parser")
    
        Download = soup.find("div", class_="downloads")
        img_url = Download.find("a")["href"]
    
        description = soup.find("div", class_="description")
        download_image_url = description.find("a")["href"]
    
        download_img_urls.append({"title": title, "download_url": hemis_url+download_image_url})
        hemis_img_urls.append({"title": title, "img_url": hemis_url+img_url})

##add to new list
    mars_data = {
        "Todays_date" : todays_date,
        "news_t": news_t,
        "news_p": news_p,
        "feat_image_url": feat_image_url,
        "mars_facts": tables,
        "hemisphere_image_urls": hemis_img_urls,
        "download_image_urls" : download_img_urls
    }

# Close the browser after scraping
    browser.quit()

# Return results
    return mars_data
