"""File containing utilities for `IO` and constants"""
from urllib.parse import quote_plus
import requests
from bs4 import BeautifulSoup
from . import urls
from . import exceptions

MONTH = {"stycznia": 1,
         "lutego": 2,
         "marca": 3,
         "kwietnia": 4,
         "maja": 5,
         "czerwca": 6,
         "lipca": 7,
         "sierpnia": 8,
         "września": 9,
         "października": 10,
         "listopada": 11,
         "grudnia": 12}

SEX = {"Kobieta": False, "Mężczyzna": True}

def parseSite(requestObj):
    """Returns object as BeautifulSoup class"""
    page = BeautifulSoup(requestObj, "html5lib")
    return page


def urlEncode(url):
    """Encode url, mainly for encoding queries."""
    return quote_plus(url)


class Defaults():
    """Some defaults for IO"""

    login_headers = {
        "Referer": urls.LOGIN,
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0"
    }
    headers = {
        "Accept-Encoding": "gzip",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0"
    }
    proxies = {}
    headers = {}


class TekstowoSession():
    """Utilities class, for user auth."""

    __jar__ = requests.Session()
    isLogged = False
    username = None

    def __init__(self, login=None, password=None):
        if(login is None or password is None):
            return
        self.login(login, password)

    def login(self, login, password):
        """Login to site using HTTP"""
        # if logged in, it wouldnt even let you login again
        if not self.isLogged:
            payload = {"login": login, "haslo": password}
            self.__jar__ = requests.sessions.Session()
            ret = self.__jar__.post(urls.LOGIN,
                                    data=payload,
                                    headers=Defaults.login_headers,
                                    proxy=Defaults.proxies)
            # when login is succesful it redirects to /, if bad it stays at /logowanie.html
            # ~~i could also check if session cookie is set, but i think this
            # also should work~~. it doesent work, session cookie is set immediately
            # on first page lookup, later its just assigned as logged in.
            if ret.ok:
                if ret.url == urls.LOGIN:
                    raise exceptions.TekstowoUnableToLogin("Bad login or password")
                self.isLogged = True
            else:
                raise exceptions.TekstowoBadSite("ret.ok is not ok")

    def logout(self):
        """Logout your session and create new empty."""
        # can't logout when not logged in. stupid
        # technically unnecessary but better to
        if self.isLogged:
            self.__jar__.get(urls.LOGOUT)
            self.__jar__ = requests.Session()

    def __del__(self):
        self.logout()

    def get(self, url, *args, **kwargs):
        """Default get, downloads site and pumps it through parseSite"""
        return parseSite(self.rawGet(url, *args, **kwargs))

    def rawGet(self, url, *args, **kwargs):
        """Return only text from request"""
        requestObj = self.__jar__.get(url,
                                      headers=Defaults.headers,
                                      proxies=Defaults.proxies,
                                      *args, **kwargs)
        try:
            if requestObj.status_code != 200:
                raise exceptions.TekstowoBadSite("Status code != 200")
        except Exception:
            raise "No network connection, bad proxy, or bad URL"
        return str(bytes(requestObj.text, "ISO-8859-1"), "utf-8").strip("\n")
