import requests
from bs4 import BeautifulSoup


class Utils:
    """Utilities class,
    to add proxies and headers overwrite Utils.proxies and Utils.headers"""
    proxies = {}
    headers = {}

    def getWebsite(self, url):
        """Download page and return it as BeautifulSoup class"""
        RAWpage = requests.get(url, proxies=self.proxies, headers=self.headers)
        print("LOG: {}".format(url))
        try:
            if RAWpage.status_code != 200:
                raise("Status code != 200")
        except Exception:
            raise("No network connection, bad proxy, or bad URL")
        RAWpage = str(bytes(RAWpage.text, "ISO-8859-1"), "utf-8").strip("\n")
        page = BeautifulSoup(RAWpage, "html5lib")
        return page
