from . import utils
from . import searchEntry
from . import urls
from overrides import overrides


class _Search():
    """Search class used to interact with search capability of website.
    Whole mechanic of search is here, only thing to change is way of
    creating entry objects
    Local variables:
     - nameOfSearch (str)
     - entries (list) containing SongEntry or ArtistEntry"""

    url = "To overwrite"
    __utils = utils.Utils()

    def __init__(self, name):
        self.nameOfSearch = name
        self.entries = []
        self.search()

    def __getitem__(self, n):
        return self.entries[n]

    def __iter__(self):
        return self.entries.__iter__()

    def __repr__(self):
        return "{}".format(str(self.__class__))

    def search(self):
        page = self.__utils.getWebsite(self.url.format(self.nameOfSearch))
        for i in page.find_all("div", "content")[0].find_all("div", "box-przeboje"):
            self.entries.append(self.createObject(i.a.get("title"), i.a.get("href")))

    def createObject(self, name, url):
        """To overwrite"""
        pass


class ArtistSearch(_Search):
    """Not much here for documentation, go see _Search"""

    def __init__(self, name):
        self.url = urls.artist_search.format(utils.urlEncode(name))
        super().__init__(name)

    def __str__(self):
        return "ArtistSearchObject {}".format(self.nameOfSearch)

    @overrides
    def createObject(self, name, url):
        return searchEntry.ArtistEntry(name, url)


class SongSearch(_Search):
    """Not much here for documentation, go see _Search"""

    def __init__(self, name):
        self.url = urls.song_search.format(utils.urlEncode(name))
        super().__init__(name)

    def __str__(self):
        return "SongSearchObject {}".format(self.nameOfSearch)

    @overrides
    def createObject(self, name, url):
        return searchEntry.SongEntry(name, url)
