from documentscraper.base import _get_url


def test_get_url():
    assert _get_url('/doc/test.pdf', None, 'http://foo') == 'http://foo/doc/test.pdf'
    assert _get_url('doc/test.pdf', None, 'http://foo') == 'http://foo/doc/test.pdf'
