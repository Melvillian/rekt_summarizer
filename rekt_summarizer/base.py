import requests
from bs4 import BeautifulSoup
import html2text

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
    raw_markdowns = []
    for url in urls:
        markdown = url_to_markdown(url)
        raw_markdowns.append(markdown)

    return raw_markdowns

def extract_main_article_text(markdowns):

    sep = '## SUBSCRIBE NOW'

    article_markdown = []
    for markdown in markdowns:
        split_markdown = markdown.split(sep, 1)
        if len(split_markdown) != 2:
            print(f"Multiple SUBSCRIBE NOWs in: {url}")
            return None
        text = split_markdown[0]
        article_markdown.append(text)
    return article_markdown

def main(urls):

    raw_markdowns = batch_url_to_markdowns(urls)

    markdowns = extract_main_article_text(raw_markdowns)

    print(markdowns[0])

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
