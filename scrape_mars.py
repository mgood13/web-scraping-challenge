from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd

def scrape():
    executable_path = {"executable_path": "/Users/michael/Desktop/UPENN_Class_Directory/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)
    scraped_dictionary = {}

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    scraped_dictionary['article_dictionary'] = {}

    # The UL items_list is the list which contains all of the articles
    news_list = soup.find('ul', class_= 'item_list')

    # Pull out the list items
    articles = news_list.find_all('li')

    # Take only the newest article
    newest_article = articles[0]

    # Take the article date... just because
    article_date = newest_article.find('div', class_ = 'list_date').text

    scraped_dictionary['article_dictionary']['date'] = article_date

    # Take the title and extract its text from the anchor
    news_title_div = newest_article.find('div', class_ = 'content_title')
    news_title = news_title_div.find('a').text

    scraped_dictionary['article_dictionary']['title'] = news_title

    # Take the "teaser" text from the article.
    news_p = newest_article.find('div', class_ = 'article_teaser_body').text

    scraped_dictionary['article_dictionary']['text'] = news_p

    # Images
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(2)

    browser.links.find_by_partial_text('FULL IMAGE').click()
    browser.links.find_by_partial_text('more info').click()

    base_url = 'https://www.jpl.nasa.gov'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    scraped_dictionary['featured_dictionary'] = {}

    whole_page = soup.find('div', id="page")
    image = whole_page.find('figure', class_='lede')
    image_url = image.find('img')['src']
    image_title = image.find('img')['title']

    full_url = base_url + image_url

    scraped_dictionary['featured_dictionary']['url'] = full_url
    scraped_dictionary['featured_dictionary']['title'] = image_title

    marsfact_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(marsfact_url)

    summary_table = tables[0]

    summary_table = summary_table.rename(columns={0: 'Parameter', 1: 'Value'})

    summary_table
    table_string = summary_table.to_html(index = False)

    table = table_string.split('\n')
    temp = []
    count = 0
    for x in table:
        if '<tr>' in x:
            count += 1
            if count % 2 == 0:
                temp.append('    <tr class = "evenrow">')
            else:
                temp.append('    <tr class = "oddrow">')
        elif '<tr style' in x:
            temp.append('    <tr style = "text-align: center">')
        elif '<table ' in x:
            temp.append('<table class = "dataframe">')
        else:
            temp.append(x)

    table = temp
    table_string = '\n'.join(table)


    scraped_dictionary['table_string'] = table_string

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    links = soup.find_all('div', class_ = 'item')
    items = len(links)
    hemisphere_list = []

    for i in range(items):
        hemisphere_dict = {'title':"",'img_url':""}
        link_title = links[i].find('h3').text
        title_list = link_title.split(' ')
        image_title = ""
        for word in title_list[:-1]:
            image_title = image_title + " " + word
        hemisphere_dict['title'] = image_title
        browser.links.find_by_partial_text('Hemisphere Enhanced').click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        lists = soup.find_all('li')
        img_url = lists[0].find('a')['href']
        hemisphere_dict['img_url'] = img_url
        hemisphere_list.append(hemisphere_dict)

    scraped_dictionary['hemisphere_list'] = hemisphere_list

    browser.quit()

    return scraped_dictionary