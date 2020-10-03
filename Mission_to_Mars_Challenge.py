#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


# In[2]:


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)


# ### Visit the NASA Mars News Site

# In[3]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
# searches for specific combo of element and also tells browser to wait 1 second before searching
# as some websites take a moment to fully load
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[4]:


# set up the HTML parser

html = browser.html
news_soup = soup(html, 'html.parser')

# the code 'ul.item_list li.slide' pinpoints the <li /> tag with the class of slide and the <ul /> tag with a class of item_list
slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[5]:


# begin scraping for article info
# chained command 'find' onto previously created variable - saying look inside this variable to find this specific info
# we want the content title inside the div class
slide_elem.find("div", class_='content_title')


# In[6]:


# Use the parent element to find the first `a` tag and save it as `news_title`
# gettext() returns just the text of an element, without html tags etc
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[7]:


# Use the parent element to find the paragraph text
# parent element is the variable slide_elem because it contains the main tag <ul /> and all the other tags within it
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### JPL Space Images Featured Images

# In[8]:


# We're trying to get the full-sixed image, and it takes a couple clicks
# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# In[10]:


# Find the more info button and click that
# Splinter can search for an html element by text
browser.is_element_present_by_text('more info', wait_time=1)

# this will take the 'more info' string to find the link associated with the 'more info' text and put it in a variable
more_info_elem = browser.links.find_by_partial_text('more info')

# we tell splinter to use the variable to click that link
more_info_elem.click()


# In[11]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[12]:


# Find the relative image url

# tells Beautiful Soup to look inside the <'figure class='lede /> tag
# for and <a /> tag and then look within that for an <img /> tag
# "this is where the image we want lives, use the link inside"

img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel

# We were able to pull the link to the image by pointing BeautifulSoup to where the image will be, 
# instead of grabbing the URL directly. This way, when NASA updates its image page, our code will 
# still pull the most recent image.


# In[13]:


# But if we copy and paste this link into a browser, it won't work. This is because it's only a partial link, as the base URL isn't included.

# Use the base URL to create an absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# ### Mars Facts

# In[14]:


# Instead of scraping each row, or the data in each <td />, we're going to scrape the entire table with Pandas' .read_html() function

# create new dataframe from the html table at this url. It searches for and returns a list of tables found in the html
# specifying the 0 index returns the first table in the list and turns it into a dataframe
df = pd.read_html('http://space-facts.com/mars/')[0]

# assigns columns to the new df
df.columns=['Description', 'Mars']

# turns the description column into the index. inplace = true means that the updated index will remain in place, 
# without having to reassign the DataFrame to a new variable.
df.set_index('Description', inplace=True)
df


# In[15]:


# renders the df back into html so we can put it on a website later

df.to_html()


# ### Mars Weather

# In[16]:


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# In[17]:


# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# In[18]:


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# ## D1: Scrape High-Resolution Mars' Hemisphere Images and Titles
# 
# #### Hemispheres

# In[19]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

# First, get a list of all of the hemispheres
hemisphere_image_urls = []

links = browser.find_by_css("a.product-item h3")

# loop through those links, click the link, find the sample button, return the href
for i in range(len(links)):
    hemisphere = {}
    
    # We have to find the elements on each loop to avoid a stale element exception
    browser.find_by_css("a.product-item h3")[i].click()
    
    # Next, we find the Sample image anchor tag and extract the href
    sample_link = browser.links.find_by_text('Sample').first
    hemisphere['img_url'] = sample_link['href']
    
    # Get Hemisphere title
    hemisphere['title'] = browser.find_by_css("h2.title").text
    
    # Append hemisphere object to list
    hemisphere_image_urls.append(hemisphere)
    
    # Finally, we navigate backwards
    browser.back()

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[22]:


# quits splinter browser so it doens't run in the background waiting for instuctions and killing your memory
browser.quit()

