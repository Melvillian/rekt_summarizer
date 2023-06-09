
# rekt_summarizer

A python script that uses the [rekt.news leaderboard](https://rekt.news/leaderboard/) and GPT-4 to categorize the hacks for all protocols on the leaderboard

![frontend](./histogram.png)

## Installation

```bash
# install deps
pip install -r requirements.txt

# set your OPENAI API key you'll use for inference
`echo "OPENAI_API_KEY=sk-YOUR_KEY" > .env`
```

## Usage

### Category and Backlink Generation

```bash
$ python -m rekt_summarizer
#or
$ rekt_summarizer
```

This will:
1. Fetch the rekt.news articles listed in their [leaderboard](https://rekt.news/leaderboard/)
2. Convert the HTML articles to markdown and store them in [rekt_summarizer/data/rekt_news_markdown/](./rekt_summarizer/data/rekt_news_markdown/)
3. Use OpenAI to categorize the hacks involved in each article such the script prints a dict of the form:


```js
{
  'categories': {
    'contract_manipulation': 75,
    'reentrancy_attack': 30,
  },
  'backlinks': {
    'contract_manipulation': ["https://rekt.news/merlin3-rekt/", "https://rekt.news/beanstalk-rekt/"],
    'human_error': ["https://rekt.news/ronin-rekt/", "https://rekt.news/beanstalk-rekt/"], "rugpull": ["https://rekt.news/ronin-rekt/"]
  }
}
```

### Streamlit Data Visualizer

```bash
streamlit run app.py
```
