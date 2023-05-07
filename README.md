
# rekt_summarizer

[![codecov](https://codecov.io/gh/Melvillian/rekt_summarizer/branch/main/graph/badge.svg?token=rekt_summarizer_token_here)](https://codecov.io/gh/Melvillian/rekt_summarizer)
[![CI](https://github.com/Melvillian/rekt_summarizer/actions/workflows/main.yml/badge.svg)](https://github.com/Melvillian/rekt_summarizer/actions/workflows/main.yml)

Awesome rekt_summarizer created by Melvillian

## Installation

```bash
# install deps
pip install -r requirements.txt

# set your OPENAI API key you'll use for inference
`echo "OPENAI_API_KEY=sk-YOUR_KEY" > .env`
```

## Usage

```bash
$ python -m rekt_summarizer
#or
$ rekt_summarizer
```

This will:
1. Fetch the rekt.news articles listed in their [leaderboard](https://rekt.news/leaderboard/)
2. Convert the HTML articles to markdown and store them in [rekt_summarizer/markdown_data/](./rekt_summarizer/markdown_data/)
3. Use OpenAI to categorize the hacks involved in each article such the script prints a dict of the form:


```js
{
  categories: {
    contract_manipulation: 75,
    reentrancy_attack: 30,
    ...
  },
  backlinks: {
    merlin3_rekt: {
      url: "https://rekt.news/merlin3-rekt/",
      categories: [
        "contract_manipulation"
      ]
    },
    safedollar_rekt: {
      url: "https://rekt.news/safedollar-rekt/",
      categories: [
        "polygon",
        "contract_manipulation"
      ]
    },
    ...
  }
}