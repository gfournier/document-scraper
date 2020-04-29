import abc
import logging
import re
import time
from urllib.parse import urljoin, quote

import requests
from lxml import html

from documentscraper.config import Config, XPathExpression, Form, Item


class ScraperEngineBase(metaclass=abc.ABCMeta):
    """
    Base class for engines. Defines contract for navigation methods.

    "rootUrl": ,
    "baseUrl": ,
    "form": {
        "method": "GET",
    "item" : [{
        "selector":
        },
        "output": {
            "id": ,
            "metadata":
                "author": ,
                "date": ,
        },
        "fields": [
        ]
    ]
    "next_page": {
    }
    """

    @abc.abstractmethod
    def get_page(self, url: str):
        """
        Loads the specified URL and
        :param url:
        :return:
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def get_element(self, page, xpath: str):
        """
        Returns an element by XPath expression.
        :param page: current page object
        :param xpath: XPath expression
        :return: the found element or None if not found
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def navigate(self, page, element):
        """
        Navigate to the specified element.
        :param page: current page object
        :param element: the element to navigate
        :return: a new page object
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def as_string(self, element):
        """
        Returns a string representation of a given element.
        :param element: a page element
        :return: a string representation of the passed element
        """
        raise NotImplementedError()


def _get_url(url_path, regex, base_url):
    url = url_path
    if regex is not None:
        url = re.match(regex, url_path)[0]
    if not url.startswith('http://'):
        url = urljoin(base_url, url)
    return url


class DocumentScraper:

    def __init__(self, engine: ScraperEngineBase, wait_interval=None, verbose=False):
        """
        Instantiates a new document scraper with the specified engine.
        :param engine: browser engine, must be a subclass of ScraperEngineBase
        :param wait_interval: interval (seconds) for refresh between pages
        """
        self.engine = engine
        self.wait_interval = wait_interval
        self.verbose = verbose
        self.logger = logging.getLogger("documentscraper")

    def _log_navigate(self, url):
        if self.verbose:
            self.logger.info(f"Navigate to: {url}")

    def run(self, config: Config, output_path=None):
        self._log_navigate(config.root_url)
        page = self._get_first_page(config.root_url, config.form)
        while page is not None:
            items = self._scrap_items(page, config.root_url, config.item)
            page = self._get_next_page(page, config.base_url, config.next_page)

    def _get_first_page(self, url: str, form: Form):
        if form is None:
            return self.engine.get_page(url)
        elif form.method == "GET":
            # Build query string: url?name1=value1&name2=value2
            query_string = "&".join([f"{field.name}={quote(str(field.value))}" for field in form.fields])
            query_url = f"{url}?{query_string}"
            return self.engine.get_page(query_url)
        else:
            raise NotImplementedError(f"Form method [{form.method}] not handled.")

    def _get_next_page(self, current_page, base_url: str, next_page: XPathExpression):
        element = self.engine.get_element(current_page, next_page.xpath)
        if element is None:
            return None
        if next_page.regex is not None and not isinstance(element, str):
            raise ValueError(f"Cannot configure an regex on an element that is not a str: {element}")
        if isinstance(element, str):
            url = _get_url(element, next_page.regex, base_url)
            self._log_navigate(url)
            return self.engine.get_page(url)
        else:
            self._log_navigate(self.engine.as_string(element))
            return self.engine.navigate(current_page, element)

    def _wait(self):
        if self.wait_interval is not None:
            time.sleep(self.wait_interval)

    def _scrap_items(self, page, root_url, item_config:Item):

        results = page.xpath(item_config.selector)
        count = 0
        for result in results:
            count = count+1
            links = result.xpath(item_config.navigation[0])
            article_url= links[0].xpath("@href")
            doc_tree2 = self.engine.get_page(article_url[0])
            author = doc_tree2.xpath(item_config.output.metadata["author"].xpath)
            print(author[0].text)
            #title =
            date= doc_tree2.xpath(item_config.output.metadata["date"].xpath)
            print(date[0].text.strip())
            # récupérer PDF

        # Get all items from the result list
        # For each item:
        #  - navigate to sub page
        #  - in sub page look for metadata
        # ( - in sub page look for documents)
        # Reload previous page ?
        return []
