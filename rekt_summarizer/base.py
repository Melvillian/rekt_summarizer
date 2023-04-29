import requests
import time
from bs4 import BeautifulSoup
import html2text

REKT_NEWS_BASE_URL = "https://rekt.news"
REKT_NEWS_PAGINATION_URL = "https://rekt.news/?page={index}"

def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching URL: {url}")
        print(e)
        return None

def extract_article(html):
    soup = BeautifulSoup(html, "html.parser")
    article = soup.find("article")
    return str(article) if article else ""

def convert_to_markdown(html):
    converter = html2text.HTML2Text()
    converter.ignore_links = False
    return converter.handle(html)

def url_to_markdown(url):
    html = fetch_html(url)
    if html is None:
        print(f"Error fetching HTML from {url}")
        return None
    article_html = extract_article(html)
    if not article_html:
        print(f"No article found at URL: {url}")
        return None

    markdown = convert_to_markdown(article_html)
    return markdown

def batch_url_to_markdowns(urls):
    raw_markdowns_and_urls = []
    for url in urls:
        markdown = url_to_markdown(url)
        raw_markdowns_and_urls.append((url, markdown))

    return raw_markdowns_and_urls

def extract_main_article_text(markdowns):

    sep = '## SUBSCRIBE NOW'

    article_markdown_and_urls = []
    for (url, markdown) in markdowns:
        split_markdown = markdown.split(sep, 1)
        if len(split_markdown) != 2:
            print(f"Multiple SUBSCRIBE NOWs in: \n{markdown}")
            return None
        text = split_markdown[0]
        article_markdown_and_urls.append((url, text))
    return article_markdown_and_urls

def gather_links_from_single_page(url):
    """
    extract all the individual rekt.news article URLs from the leaderboards page
    """

    try:
        response = requests.get(url)
        response.raise_for_status()
        html = response.text

        soup = BeautifulSoup(html, "html.parser")
        titles = soup.find_all(class_="leaderboard-row-title")
        
        article_urls = []
        for title in titles:
            article_urls.append(REKT_NEWS_BASE_URL + title.a['href'])

        return article_urls

    except requests.RequestException as e:
        print(f"Error fetching URL: {url}")
        print(e)
        return None

def extract_article_urls_from_leaderboard_page():
    return gather_links_from_single_page("https://rekt.news/leaderboard/")

def main(urls):
    urls = extract_article_urls_from_leaderboard_page()

    raw_markdowns_and_urls = batch_url_to_markdowns(urls)

    article_markdown_and_urls = extract_main_article_text(raw_markdowns_and_urls)

    print(article_markdown_and_urls[0])

    # TODO
    # (categories, backlinks) = categorize_markdowns_with_backlinks(markdowns)

    # print("CATEGORIES:")
    # print(categories)
    # print("BACKLINKS:")
    # print(backlinks)

if __name__ == "__main__":
    urls = [
        "https://rekt.news/merlin-dex-rekt/",
        # Add more URLs if needed
    ]
    main(urls)
