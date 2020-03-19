import logging
from documentscraper import load_config, DocumentScraper, RequestsScraperEngine

logging.basicConfig(level=logging.DEBUG)

config = load_config("./arxiv.json")
scraper = DocumentScraper(RequestsScraperEngine(), verbose=True)
scraper.run(config, output_path=None)
