import requests
from bs4 import BeautifulSoup
from copy import copy


def parseSite(requestObj):
    try:
        if requestObj.status_code != 200:
            raise Exception("Status code != 200")
    except Exception:
        raise("No network connection, bad proxy, or bad URL")
    requestObj = str(bytes(requestObj.text, "ISO-8859-1"), "utf-8").strip("\n")
    page = BeautifulSoup(requestObj, "html5lib")
    return page


class Defaults():
    _login_headers = {
        "Referer": "https://www.tekstowo.pl/logowanie.html",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0"
    }
    _use_headers = {
        "Accept-Encoding": "gzip",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0"
    }
    proxies = {}
    headers = {}


class TekstowoSession():
    """Utilities class, for user auth."""

    __jar = None
    is_logged = False
    username = None

    def __init__(self, login=None, password=None):
        if(login is None or password is None):
            return
        self.login(login, password)

    def login(self, login, password):
        # won't relogin, PHPSESS is still valid
        # if logged in, it wouldnt even let you login again (i think)
        if(not self.is_logged):
            payload = {"login": login, "haslo": password}
            self.__jar = requests.sessions.Session()
            ret = self.__jar.post("https://www.tekstowo.pl/logowanie.html",
                                  data=payload,
                                  headers=Defaults._login_headers)
            # when login is succesful it redirects to /, if bad it stays at /logowanie.html
            # i could also check if session cookie is set, but i think this
            # also should work
            if(ret.ok):
                if(ret.url == "http://www.tekstowo.pl/logowanie.html"):
                    raise Exception("Couldn't log in.")
                self.is_logged = True
            else:
                raise Exception("Couldn't log in.")

    def __logout(self):
        # can't logout when not logged in. stupid
        # technically unnecessary but better
        if(self.is_logged):
            self.__jar.get("https://www.tekstowo.pl/wyloguj.html")
            self.__jar = None

    def __del__(self):
        self.__logout()

    def get(self, url, *args, **kwargs):
        return self.__jar.get(url, *args, **kwargs)


class Utils:
    """Utilities class,
    to add proxies and headers overwrite Utils.proxies and Utils.headers"""
    __jar = None

    def __init__(self, jar=None):
        self.__jar = jar

    def getWebsite(self, url, jar=None, *args, **kwargs):
        """Download page and return it as BeautifulSoup class"""
        all_headers = copy(Defaults._use_headers)
        all_headers.update(Defaults.headers)
        if(not jar):
            RAWpage = requests.get(url, proxies=Defaults.proxies, headers=all_headers)
        elif(self.__jar):
            RAWpage = jar.get(url, proxies=Defaults.proxies, headers=all_headers)
        elif(type(jar) == TekstowoSession):
            RAWpage = jar.get(url, proxies=Defaults.proxies, headers=all_headers)
        else:
            raise Exception("Passed bad jar object")
        # print("LOG: {}".format(url))

        return parseSite(RAWpage)
