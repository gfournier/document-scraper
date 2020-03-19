import requests

from documentscraper.base import ScraperEngineBase


class RequestsScraperEngine(ScraperEngineBase):

    def get_page(self, url: str):
        response = requests.get(url)
        response.raise_for_status()
        return response.content

    def get_element(self, page, xpath: str):
        pass

    def navigate(self, page, element):
        pass

    def as_string(self, element):
        pass
