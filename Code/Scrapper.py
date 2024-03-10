import json
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from requests_html import HTMLSession


def scrape_climate_change_news(url, session):
    response = session.get(url)
    response.html.render(timeout=30)
    time.sleep(5)

    soup = BeautifulSoup(response.html.html, 'html.parser')

    if 'climatechangenews' in url:
        articles = soup.find_all('div', class_='media')
    elif 'news.un.org' in url:
        articles = soup.find_all('div', class_='views-row')
    elif 'apnews' in url:
        articles = soup.find_all('div', class_='PageList-items-item')

    for article in articles:
        if 'apnews' in url:
            title_element = article.find('h3')
            date_element = article.select_one('span[data-date]')
        else:
            title_element = article.find('h2')
            date_element = article.find('time')

        a_element = article.find('a')

        title_text = title_element.text.strip() if title_element else 'No Title'
        date_text = date_element.text.strip() if date_element else 'No Date'

        if a_element:
            href = a_element['href']

            # Check if href is a complete URL or needs to be joined
            if 'news.un.org' in url:
                if not href.startswith(('http://', 'https://')):
                    href = urljoin("https://news.un.org", href)
            else:
                if not href.startswith(('http://', 'https://')):
                    href = urljoin(url, href)  

            # Make a request to the nested href
            nested_response = session.get(href)
            nested_response.html.render(timeout=30)
            time.sleep(5)
            nested_soup = BeautifulSoup(nested_response.html.html, 'html.parser')

            # Find the div with class 'news-content'
            if 'climatechangenews' in url:
                news_content_div = nested_soup.find('div', class_='news-content')
            elif 'news.un.org' in url:
                news_content_div = nested_soup.find('div', class_='clearfix text-formatted field field--name-field-text-column field--type-text-long field--label-hidden field__item')
            elif 'apnews' in url:
                news_content_div = nested_soup.find('div', class_='RichTextStoryBody RichTextBody')

            # Extract text from all paragraph tags inside 'news-content'
            paragraphs = news_content_div.find_all('p') if news_content_div else []
            description_text = ' '.join([p.text.strip() for p in paragraphs])

            # Extract image URLs
            article_img = [img['src'] for img in news_content_div.find_all('img')] if news_content_div else []

            # Create a dictionary for each article
            article_info = {
                'Title': title_text,
                'Date': date_text,
                'Description': description_text,
                'Images': article_img,
                'Link': href,
            }

            # Append the dictionary to the list
            article_list.append(article_info)


 # List to store article information
article_list = []

def scrap():
    # List of URLs to scrape
    """urls = [
        'https://news.un.org/en/news/topic/climate-change',
        'https://apnews.com/hub/climate-change',
        'https://www.climatechangenews.com/',
    ]"""
    urls = [
        'https://news.un.org/en/news/topic/climate-change'
    ]

    session = HTMLSession()

    for url in urls:
        scrape_climate_change_news(url, session)

    # Convert the list of dictionaries to a JSON object
    # json_object = json.dumps(article_list, indent=2)
    # return json_object
    return article_list