from overrides import overrides
from . import utils
from . import searchEntry
from . import urls
from . import exceptions


class _Search():
    """Search class used to interact with search capability of website.
    Whole mechanic of search is here, only thing to change is way of
    creating entry objects
    Local variables:
     - nameOfSearch (str)
     - entries (list) containing SongEntry or ArtistEntry"""

    url = ""

    def __init__(self, name, session=None):
        if not isinstance(session, utils.TekstowoSession):
            raise exceptions.TekstowoBadObject("Passed wrong object.")
        self.session = session
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
        page = self.session.get(self.url.format(self.nameOfSearch))
        for i in page.find_all("div", "content")[0].find_all("div", "box-przeboje"):
            self.entries.append(self.createObject(i.a.get("title"), i.a.get("href")))

    def createObject(self, name, url):
        """To overwrite"""


class ArtistSearch(_Search):
    """Not much here for documentation, go see _Search"""
    __slots__ = ["nameOfSearch", "entries", "session", "url"]

    def __init__(self, name, *args, **kwargs):
        self.url = urls.artist_search.format(utils.urlEncode(name))
        super().__init__(name, *args, **kwargs)

    def __str__(self):
        return "ArtistSearchObject {}".format(self.nameOfSearch)

    @overrides
    def createObject(self, name, url):
        return searchEntry.ArtistEntry(name, url, self.session)


class SongSearch(_Search):
    """Not much here for documentation, go see _Search"""
    __slots__ = ["nameOfSearch", "entries", "session", "url"]

    def __init__(self, name, *args, **kwargs):
        self.url = urls.song_search.format(utils.urlEncode(name))
        super().__init__(name, *args, **kwargs)

    def __str__(self):
        return "SongSearchObject {}".format(self.nameOfSearch)

    @overrides
    def createObject(self, name, url):
        return searchEntry.SongEntry(name, url, self.session)
