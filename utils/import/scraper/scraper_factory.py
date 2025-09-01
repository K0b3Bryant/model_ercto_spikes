import yaml
from scraping_engine import ScrapingEngine
from parsers.generic_parser import GenericListParser


PARSER_MAPPING = {
    "GenericListParser": GenericListParser,
    # Add new parser classes here
}

def load_config(path="config/scrapers.yaml"):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def get_scraper(scraper_name: str, config_path="config/scrapers.yaml"):
    """ Factory function to create a scraper instance. """
    config = load_config(config_path)
    scraper_config = config.get("scrapers", {}).get(scraper_name)

    if not scraper_config:
        raise ValueError(f"Scraper '{scraper_name}' not found in configuration.")

    ParserClass = PARSER_MAPPING.get(scraper_config['parser_class'])
    if not ParserClass:
        raise ValueError(f"Unknown parser class '{scraper_config['parser_class']}'.")

    engine = ScrapingEngine()
    return ParserClass(engine, scraper_config)
