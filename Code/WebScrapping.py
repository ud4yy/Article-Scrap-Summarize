import json
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from requests_html import HTMLSession
# from sentence_transformers import SentenceTransformer
# from sklearn.metrics.pairwise import cosine_similarity

# def calculate_cosine_similarity(embedding1, embedding2):
#     return cosine_similarity(embedding1, embedding2)[0][0]

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

# Load SentenceTransformer model
# model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

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

# List to store article information
article_list = []

for url in urls:
    scrape_climate_change_news(url, session)
    # Add more conditions for other websites if needed

# # Compare titles and merge similar articles
# for i in range(len(article_list) - 1, -1, -1):
#     for j in range(i - 1, -1, -1):
#         embedding1 = model.encode([article_list[i]['Title']])[0].reshape(1, -1)
#         embedding2 = model.encode([article_list[j]['Title']])[0].reshape(1, -1)
#         similarity = calculate_cosine_similarity(embedding1, embedding2)
#         if similarity > 0.8:  # Set your desired similarity threshold
#             article_list[i]['Description'] += article_list[j]['Description']
#             article_list[i]['Images'].extend(article_list[j]['Images'])
#             del article_list[j]

# Convert the list of dictionaries to a JSON object
json_object = json.dumps(article_list, indent=2)

# Save the JSON object to a file
with open('newarticles.json', 'w') as json_file:
    json_file.write(json_object)

print('JSON file saved as articles.json')
