import sys
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

def main(urls):

    # TODO: refactor into its own function
    raw_markdowns = []
    for url in urls:
        html = fetch_html(url)
        if html is None:
            continue

        article_html = extract_article(html)
        if not article_html:
            print(f"No article found at URL: {url}")
            continue

        markdown = convert_to_markdown(article_html)
        print("OUTPUT:")
        print(markdown)
        print("END\n")
        raw_markdowns.append(markdown)


    # TODO
    markdowns = extract_main_article_text(raw_markdowns)

    # TODO
    (categories, backlinks) = categorize_markdowns_with_backlinks(markdowns)

    print("CATEGORIES:")
    print(categories)
    print("BACKLINKS:")
    print(backlinks)

if __name__ == "__main__":
    urls = [
        "https://rekt.news/merlin-dex-rekt/",
        # Add more URLs if needed
    ]
    main(urls)
