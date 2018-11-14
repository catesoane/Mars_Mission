# Import Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
from selenium import webdriver
import os
import pandas as pd
import requests
import time 
import tweepy
# from config import (consumer_key, 
#                     consumer_secret, 
#                     access_token, 
#                     access_token_secret)


# NASA MARS NEWS
def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # Create a dictionary for all scraped data
    mars_data = {}

    # Visit the NASA news URL
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # Search for news / scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find most recent article, title and date
    article = soup.find("div", class_="list_text")
    news_p = article.find("div", class_="article_teaser_body").text
    news_title = article.find("div", class_="content_title").text
    news_date = article.find("div", class_="list_date").text

    # Add most recent article, title and data to dict
    mars_data["news_date"] = news_date
    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p

    # JPL MARS SPACE IMAGES - FEATURED IMAGE
    # Visit the JPL Mars URL 
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)

    # Scrape the browser into soup and use soup to find the image of mars
    # Save the image url to a variable called `img_url`
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image = soup.find("img", class_="thumb")["src"]
    img_url = "https://jpl.nasa.gov"+image
    featured_image_url = img_url

    # Add featured image url to dict
    mars_data["featured_image_url"] = featured_image_url

    # MARS WEATHER
    # Scrape weather tweet from Twitter
    # auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # auth.set_access_token(access_token, access_token_secret)
    # api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    for text in browser.find_by_css('.tweet-text'):
        if text.text.partition(' ')[0] == 'Sol':
            mars_weather = text.text
            break

    # Add weather to dict
    mars_data["mars_weather"] = mars_weather

    # MARS FACTS
    # Visit the Mars facts webpage and scrape table data into Pandas
    url3 = "http://space-facts.com/mars/"
    browser.visit(url3)

    table = pd.read_html(url3)
    mars_df = pd.DataFrame(table[0])
    mars_df.columns = ["Mars", "Data"]
    mars_df_clean = mars_df.set_index(["Mars"])
    mars_html_table = mars_df_clean.to_html(classes='mars_html_table')
    mars_html_table = mars_html_table.replace("\n", "")

    # Add Mars facts table to dict
    mars_data["mars_table"] = mars_html_table

    # MARS HEMISPHERES
    # Visit the USGS Astogeology site and scrape pictures of the hemispheres
    url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url4)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_hemis=[]

    for i in range (4):
        time.sleep(5)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        partial = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary={"title":img_title,"img_url":img_url}
        mars_hemis.append(dictionary)
        browser.back()

    mars_data["mars_hemis"] = mars_hemis

    return mars_data
          
