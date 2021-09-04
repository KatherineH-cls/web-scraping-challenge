# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'


# Dependencies
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def scrape_info():
    # %%
    # NASA MARS NEWS
    executable_path = {'executable_path': ChromeDriverManager().install()}
    driver = webdriver.Chrome(**executable_path)

    # %%
    driver.get('https://redplanetscience.com/')
    time.sleep(2)
    # used xpath to locate the elements
    try:
        titles = driver.find_elements_by_xpath('//*[@id="news"]/div[1]/div/div[2]/div/div[2]')
        news_title = titles[0].text
        snippet = driver.find_elements_by_xpath('//*[@id="news"]/div[1]/div/div[2]/div/div[3]')
        news_p = snippet[0].text

    # exception for the times that the webpage does not load properly
    except:
        news_title ="NASA to Broadcast Mars 2020 Perseverance Launch, Prelaunch Activities"
        news_p = "Starting July 27, news activities will cover everything from mission engineering and science to returning samples from Mars to, of course, the launch itself."

    # %%
    # close the driver browser
    driver.close()

    # %% [markdown]
    # # JPL Mars Space Images - Featured Image

    # %%
    # use splinter  and beautiful soup for this exercise
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # %%
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)


    # %%
    browser.links.find_by_partial_text('FULL IMAGE').click()
    html = browser.html
    soup = bs(html, 'html.parser')


    # %%
    image_location=soup.find('img', class_="headerimage fade-in")['src']
    featured_image_url = url + image_location
    


    # %%
    # Quite the browser after scraping
    browser.quit()

    # %% [markdown]
    # # Mars Facts

    # %%
    # Mars Facts Webpage
    url = 'https://galaxyfacts-mars.com/'


    # %%
    # scrape for the tables
    tables = pd.read_html(url)
    mars_facts = tables[0]

    # %%
    # convert to html for use on webpage
    facts_table = mars_facts.to_html(index = False, header = False)


    # %%
    # MARS HEMISPHERES
    # use splinter  and beautiful soup for this exercise
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # %%
    # use splinter and beautiful soup to get html
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')


    # %%
    # initialise dictionary
    hemisphere_image_urls = []

    # each hemisphere has its own section
    moons = soup.find_all('div', class_='item')
    for moon in moons:
        # title is in h3
        clean_title = moon.h3.text.strip()
        # go to page with info on full image
        moon_link = moon.a['href']
        browser.visit(url + moon_link)
        # use splinter and beautiful soup to find url of full image
        moon_html = browser.html
        moon_soup = bs(moon_html, 'html.parser')
        moon_look = moon_soup.find('div', id='wide-image')
        moon_look_again = moon_look.find('a', target='_blank')['href']
        moon_image_url = url + moon_look_again
        # add to dictionary
        hemisphere_image_urls.append({"title":clean_title, "img_url":moon_image_url})
        # return to main page
        browser.links.find_by_partial_text('Back').click()
        time.sleep(1)
            
    # %%
    
    # create dictionary of outputs
    mars_info = {
    "news_title":news_title,
    "news_p": news_p,
    "featured_img_url": featured_image_url,
    "facts":facts_table,
    "hemispheres":hemisphere_image_urls
    }

    browser.quit()

    return mars_info
