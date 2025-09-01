import json
from scraper_factory import get_scraper

def run_scraper(name, max_pages=1):
    """Helper function to run a scraper and print its results."""
    print(f"\n{'='*20} RUNNING SCRAPER: {name.upper()} {'='*20}")
    try:
        scraper = get_scraper(name)
        data = scraper.scrape(max_pages=max_pages)
        print(f"\n>>> Successfully scraped {len(data)} total items from '{name}'.")
        print(json.dumps(data[:2], indent=2))

    except Exception as e:
        print(f"An error occurred while running scraper '{name}': {e}")
        import traceback
        traceback.print_exc()

def main():
    run_scraper("hacker_news", max_pages=2) # examples - setup in config
    run_scraper("js_bookstore") # examples - setup in config

if __name__ == "__main__":
    main()
