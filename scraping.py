
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)

# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

# set up the HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')

# the code 'ul.item_list li.slide' pinpoints the <li /> tag with the class of slide and the <ul /> tag with a class of item_list
slide_elem = news_soup.select_one('ul.item_list li.slide')

# begin scraping for article info
slide_elem.find("div", class_='content_title')
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p

# ## JPL Space Images Featured Image

# We're trying to get the full-sixed image, and it takes a couple clicks
# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()

# Find the more info button and click that
# Splinter can search for an html element by text
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url

## Mars Facts

# Instead of scraping each row, or the data in each <td />, we're going to scrape the entire table with Pandas' .read_html() function
df = pd.read_html('http://space-facts.com/mars/')[0]

# assigns columns to the new df
df.columns=['description', 'value']

# turns the description column into the index. inplace = true means that the updated index will remain in place, 
# without having to reassign the DataFrame to a new variable.
df.set_index('description', inplace=True)
df

# renders the df back into html so we can put it on a website later
df.to_html()

# quits splinter browser so it doens't run in the background waiting for instuctions and killing your memory
browser.quit()


