"""CLI interface for rekt_summarizer project.

Be creative! do whatever you want!

- Install click or typer and create a CLI app
- Use builtin argparse
- Start a web application
- Import things from your .base module
"""

from .base import main as task  # pragma: no cover



def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python -m rekt_summarizer` and `$ rekt_summarizer `.

    This is your program's entry point.

    You can change this function to do whatever you want.
    Examples:
        * Run a test suite
        * Run a server
        * Do some other stuff
        * Run a command line application (Click, Typer, ArgParse)
        * List all available tasks
        * Run an application (Flask, FastAPI, Django, etc.)
    """
    print("Beginning...")

    # TODO: make this a generic webscraper with some random time delay to avoid getting blocked
    urls = [
        "https://rekt.news/merlin-dex-rekt/",
        # Add more URLs if needed
    ]


    task(urls)

    print("Done!")
