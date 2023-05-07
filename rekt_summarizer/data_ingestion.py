import requests
import os
import time
from bs4 import BeautifulSoup
import html2text

REKT_NEWS_BASE_URL = "https://rekt.news"
REKT_NEWS_PAGINATION_URL = "https://rekt.news/?page={index}"
DATA_DIRECTORY = "rekt_summarizer/data"
MARKDOWN_DIRECTORY = f"{DATA_DIRECTORY}/rekt_news_markdown"

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

def single_url_to_markdown(url):
    if (os.path.exists(article_url_to_filepath(url))):
        print(f"skipping url: {url} because it already exists")
        return None

    # sleep so we don't get rate limited
    time.sleep(5)

    print(f"fetching url and converting to markdown: {url}")
    markdown = url_to_markdown(url)
    return (url, markdown)

def batch_url_to_markdowns(urls):
    raw_markdowns_and_urls = []
    for url in urls:
        raw_markdown_and_url = single_url_to_markdown(url)
        if (raw_markdown_and_url is not None):
            raw_markdowns_and_urls.append(raw_markdown_and_url)

    return raw_markdowns_and_urls

def single_cleanup_markdown_text(url, markdown):
    print(f"\ncleaning up the markdown for url: {url}\n")

    # remove everything after `## SUBSCRIBE NOW`, which we know to be just rekt.news footer text
    split_markdown = markdown.split('## SUBSCRIBE NOW', 1)
    markdown = split_markdown[0]

    # remove everything before the first `.png)`, which we know to be just rekt.news header text + the URL to the article's PNG header
    # note, this is error-prone, but it's the best we can do for now
    split_markdown = markdown.split(".png)", 1)
    if len(split_markdown) != 2:
        # sometimes rekt.news uses a .jpg instead of a .png for the article header image
        split_markdown = markdown.split(".jpg)", 1)
        if len(split_markdown) != 2:
            # handle https://rekt.news/warp-finance-rekt/
            if "warp-finance-rekt" not in url:
                print(f"there is some new parsing error for url: {url}")
                raise Exception("Error splitting markdown")
            split_markdown = markdown.split("two...**", 1)
    text = split_markdown[1]

    return (url, text)

def batch_cleanup_markdown_text(raw_markdowns_and_urls):
    article_markdowns_and_urls = []
    for (url, markdown) in raw_markdowns_and_urls:
        url_and_text = single_cleanup_markdown_text(url, markdown)
        article_markdowns_and_urls.append(url_and_text)
    return article_markdowns_and_urls

def extract_article_urls_from_leaderboard_page(url):
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
    

def article_url_to_filepath(url):
    """
    convert from something like "https://rekt.news/ronin-rekt/"
    to "ronin_rekt"
    """

    filename_without_extension = url.split(".news/", 1)[1].replace("/", "")
    filepath = os.path.join(MARKDOWN_DIRECTORY, f"{filename_without_extension}.md")
    return filepath
    

def single_write_markdown_to_file(url, text_content):
    filepath = article_url_to_filepath(url)

    # only create the file if it doesn't already exist
    if not os.path.exists(filepath):
        with open(filepath, "w") as file:
            file.write(text_content)

        print(f"Created file: {filepath}")

def batch_write_markdowns_to_files(article_markdown_and_urls):
    # Create the directory if it doesn't exist
    if not os.path.exists(MARKDOWN_DIRECTORY):
        os.makedirs(MARKDOWN_DIRECTORY)

    for url, text_content in article_markdown_and_urls:
        single_write_markdown_to_file(url, text_content)

def ingest_articles_and_store_as_markdown():
    """
    This is the primary function of this file. It fetches all the articles from rekt.news leaderboard,
    converts them to markdown using BeautifulSoup, and then stores them in MARKDOWN_DIRECTORY so that
    they can be used for prompt engineering
    """
    urls = extract_article_urls_from_leaderboard_page("https://rekt.news/leaderboard/")

    for url in urls:
        response = single_url_to_markdown(url)
        if response is None:
            continue
        (url, raw_markdown) = response
        (url, markdown) = single_cleanup_markdown_text(url, raw_markdown)
        single_write_markdown_to_file(url, markdown)

    raw_markdowns_and_urls = batch_url_to_markdowns(urls)

    article_markdown_and_urls = batch_cleanup_markdown_text(raw_markdowns_and_urls)

    batch_write_markdowns_to_files(article_markdown_and_urls)