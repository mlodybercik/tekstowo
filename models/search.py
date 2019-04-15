from . import utils
from . import searchEntry
from overrides import overrides


class __Search():
    """Search class used to interact with search capability of website.
    Whole mechanic of search is here, only thing to change is way of
    creating entry objects"""

    url = "To overwrite"
    __utils = utils.Utils()

    def __init__(self, name):
        self.nameOfSearch = name
        self.entries = []
        self.search()

    def search(self):
        page = self.__utils.getWebsite(self.url.format(self.nameOfSearch))
        for i in page.find_all("div", "content")[0].find_all("div", "box-przeboje"):
            self.entries.append(self.createObject(i.a.get("title"), i.a.get("href")))

    def createObject(self, name, url):
        """To overwrite"""
        pass


class ArtistSearch(__Search):
    url = """https://www.tekstowo.pl/szukaj,wykonawca,{},strona,1.html"""

    @overrides
    def createObject(self, name, url):
        return searchEntry.ArtistEntry(name, url)


class SongSearch(__Search):
    url = """https://www.tekstowo.pl/szukaj,tytul,{},strona,1.html"""

    @overrides
    def createObject(self, name, url):
        return searchEntry.SongEntry(name, url)
