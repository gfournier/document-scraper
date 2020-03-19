import abc
import logging
import re
import time
from urllib.parse import urljoin

from documentscraper.config import Config, XPathExpression


class ScraperEngineBase(metaclass=abc.ABCMeta):
    """
    Base class for engines. Defines contract for navigation methods.
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
        page = self.engine.get_page(config.root_url)
        while page is not None:
            items = self._scrap_items(page, config.root_url, None)
            page = self._get_next_page(page, config.base_url, config.next_page)

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

    def _scrap_items(self, page, root_url, item_config):
        return []
