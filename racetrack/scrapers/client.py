import requests


CHROME = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko)' \
    + ' Chrome/41.0.2228.0 Safari/537.36'


class RequestWrapper(object):
    HEADERS = {
        'User-Agent': CHROME
    }

    def get(self, url):
        return requests.get(url, headers=self.HEADERS)
