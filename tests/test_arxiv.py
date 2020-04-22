import os
import re

from lxml import html

from documentscraper import load_config


def test_arxiv_date():
    config = load_config(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'samples', 'arxiv.json'))
    html_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources', 'arxiv.html')
    with open(html_file, 'rt') as f:
        raw_html = f.read()
    tree = html.fromstring(raw_html)
    date_element = tree.xpath(config.item.output.metadata['date'].xpath)[0]
    date = re.findall(config.item.output.metadata['date'].regex, date_element.text)[0]
    assert date == '21 Apr 2020'
