import os
import time
import glob
import pickle

from .categorizer import infer_categories_from_article
from .data_ingestion import ingest_articles_and_store_as_markdown

REKT_NEWS_BASE_URL = "https://rekt.news"
REKT_NEWS_PAGINATION_URL = "https://rekt.news/?page={index}"
DATA_DIRECTORY = "rekt_summarizer/data"
MARKDOWN_DIRECTORY = f"{DATA_DIRECTORY}/rekt_news_markdown"

def get_article_url(filepath):
    # filepath = "rekt_summarizer/data/rekt_news_markdown/eminence-rekt-in-prod.md"
    article_md_file = filepath.split(MARKDOWN_DIRECTORY, 1)[1]
    # article_md_file = "/eminence-rekt-in-prod.md"
    article_name = article_md_file[:-3]
    # article_name = "/eminence-rekt-in-prod"
    article_url = REKT_NEWS_BASE_URL + article_name
    return article_url

def main():
    ingest_articles_and_store_as_markdown()

    # gather filepaths and loop through summarizing them
    markdown_filepaths = glob.glob(os.path.join(MARKDOWN_DIRECTORY, "*.md"))

    # stores the number of hacks for each category
    # e.g.: { "human_error": 5, "rugpull": 2 }
    categories = {}

    # stores the mapping between categories and the articles that categories were inferred from
    # e.g.: { "human_error": ["https://rekt.news/ronin-rekt/", "https://rekt.news/beanstalk-rekt/"], "rugpull": ["https://rekt.news/ronin-rekt/"] }
    backlinks = {}

    for filepath in markdown_filepaths:
        with open(filepath, "r") as file:
            markdown = file.read()

            print(filepath)
            article_categories = infer_categories_from_article(markdown, categories)

            # if this article had some hack categories, let's update the category dict by incrementing
            # the count for each hack
            for category in article_categories:
                category_count = categories.get(category)
                if (category_count is None):
                    categories[category] = 1
                else:
                    categories[category] = category_count + 1
            
            # update our backlinks so we can see the articles that each hack category was inferred from
            for category in article_categories:
                article_url = get_article_url(filepath)
                article_urls_for_category = backlinks.get(category)

                # update backlinks
                if article_urls_for_category is None:
                    backlinks[category] = [article_url]
                else:
                    # to be extra sure, check to make sure we don't have any duplicate
                    # categories for a given hack. An AssertionError here would mean
                    # that GPT is creating category arrays with duplicate categories
                    # which we don't want
                    if article_url in article_urls_for_category:
                        raise AssertionError(f"Duplicate category for article {article_url} and category {category}")

                    backlinks[category].append(article_url)

            # TODO: intermediate print these for debugging purposes, delete when no longer needed
            # print the categories and their counts
            print("CATEGORIES:")
            print(categories)

            print("BACKLINKS:")
            print(backlinks)

            # sleep for 10 seconds to avoid hitting the OPENAI API rate limit
            # This calculation is based on an average of 24.5 tokens per minute
            # and the rate limit is 40k tokens per minute
            time.sleep(10)
    
    result = {
        'categories': categories,
        'backlinks': backlinks
    }
    
    print(result)

    # Pickling the result so the streamlit app can use it
    with open(f"{DATA_DIRECTORY}/summarization_results.pkl", 'wb') as file:
        pickle.dump(result, file)

if __name__ == "__main__":
    main()
