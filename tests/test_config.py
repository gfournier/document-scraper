import os

from documentscraper import load_config


def test_load_config():
    config = load_config(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'samples', 'arxiv.json'))
    assert config.base_url == "https://arxiv.org"
    assert len(config.form.fields) == 5
    assert config.form.fields[0].value == "deep learning"
