# document-scraper
Scraping framework to retrieve lists of articles, like RFP websites.

## What ?

We want to scrap documents from websites that display list of documents after a search.
Here is a web site example (arXiv):
![arXiv](doc/images/arxiv.png)

The scraping tool should be configurable to allow:
* retrieval of several linked documents for each item
* retrieval of metadata for each item

We must also handle two kind of websites:
* "full html" websites that can be scraped with `requests`/`lxml` kind of tools
* "javascript" modern websites that requires tools like [Selenium](https://selenium-python.readthedocs.io/)

The image below shows the scraping workflow.
![scraping](doc/images/workflow.png)

