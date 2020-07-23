# 1. import Flask
from flask import Flask
from flask import render_template

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from bs4 import BeautifulSoup as bs
import pandas as pd #cannot import for some reason
# need to import Pymongo
import requests
from splinter import Browser

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

#add Mongo

app.config['MONGO_URI'] = "mongodb://localhost:27017/mars_data"
mongo = PyMongo(app)

# 3. Define what to do when a user hits the index route


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scrape")
def scrape():

    url = "https://mars.nasa.gov/news/"
    response = requests.get(url,verify=False)
    
    soup = bs(response.text, 'html.parser')
    title_results = soup.find_all('div', class_="content_title")
    for result in title_results:
    # Error handling
        try:
            # Identify and return title of listing
            title = result.find('a').text          

        
        except AttributeError as e:
            print(e)
   
    return render_template('scrape.html', title=title)

    # getting werid error with above. Variable can be displayed

    # Update the Mongo database using update and upsert=True
    mongo.db.mars_data.update({}, mars_data, upsert=True)

    
def get_paragraphs():

    executable_path = {'executable_path': r'C:\Users\david\Desktop\chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    paragraphs = soup.find_all("div", class_ ="article_teaser_body")

    for paragraph in paragraphs:
        paragraph_text = paragraph.text
        print(paragraph_text)
       
def image():
    
    executable_path = {'executable_path': r'C:\Users\david\Desktop\chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    img_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(img_url)
    html = browser.html
    soup = bs(html, 'html.parser')

    img_results = soup.find_all('a', id="full_image")[0]

    featured_image_url = 'https://www.jpl.nasa.gov' + img_results['data-fancybox-href']
    print (featured_image_url)

def twitter(): 

    twitter_url =  "https://twitter.com/marswxreport?lang=en"
    twitter_response = requests.get(twitter_url)
    twitter_soup = bs(twitter_response.text, 'html.parser')

    twitter_results = twitter_soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    current_tweet = twitter_results.getText()
    print(current_tweet)

def mars_facts():
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    mars_df = tables[0]

#need function for last exercise


if __name__ == "__main__":
    app.run(debug=True)
