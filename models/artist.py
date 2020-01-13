"""File containing Artist declaration."""
from bs4 import BeautifulSoup
from . import draft
from . import utils
from . import urls
from . import exceptions


class Artist:
    """Class for storing artist info and his songs.
    Local variables:
     - name (str)
     - aboutArtist (str)
     - albums (list or None)
     - amountOfFans (int)
     - songList (list with Song objects)

     Local methods:
     - None
    """
    __slots__ = ["_session", "_valid_keys", "name",
                 "aboutArtist", "albums", "amountOfFans", "songList"]

    def __init__(self, page, session=None):
        if not isinstance(page, BeautifulSoup):
            raise exceptions.TekstowoBadObject("Passed page is not a BeautifulSoup class")
        if not isinstance(session, utils.TekstowoSession):
            raise exceptions.TekstowoBadJar("Passed object is not a TekstowoSession")
        self._session = session
        self.__parse__(page)

    @classmethod
    def fromUrl(cls, url, session):
        """Create object from url"""
        return cls(session.get(url), session)

    def __str__(self):
        return "{}".format(self.name)

    def __repr__(self):
        return "{}ArtistObject".format(self.name)

    def __getitem__(self, key):
        if key.casefold() in ["a", "albums"]:
            return self.albums
        elif key.casefold() in ["s", "songlist", "songs"]:
            return self.songList
        else:
            raise Exception("Given key is not valid {}".format(key))

    def __getName__(self, page):
        """Returns artist name"""
        return page.find_all("div", "belka short")[0].strong.get_text()

    @exceptions.catchAndReturn(list)
    def __getAlbums__(self, page):
        """Returns [string] with albums"""
        albums = []
        for album in page.find(id="artist-disc").find_all("p"):
            albums.append(album.b.get_text())
        return albums

    @exceptions.catchAndReturn(str)
    def __getAboutArtist__(self, page):
        """Returns the about artist section"""
        return page.find(id="artist-desc").p.get_text()

    def __getAmountOfFans__(self, page):
        """Returns amount of "fans" from page"""
        return int(page.find_all("div", "odslon")[0].get_text().strip("Fanów: "))

    def __getSongList__(self, page):
        """Returns list of songs"""
        songs = []
        name = page.find_all("div", "left-corner")[0].find_all("a", "green")[3].get("href")[11:-5:]
        page = self._session.get(urls.ARTIST_SONGS.format(name))
        _list = page.find_all("div", "ranking-lista")[0].find_all("div", "box-przeboje")
        for _song in _list:
            a = _song.find_all("a", "title")[0] # pylint: disable=C0103
            songs.append(draft.Song(a.get("title"), a.get("href"), self._session))
        return songs

    def __parse__(self, page):
        self.name = self.__getName__(page)
        self.aboutArtist = self.__getAboutArtist__(page)
        self.albums = self.__getAlbums__(page)
        self.amountOfFans = self.__getAmountOfFans__(page)
        self.songList = self.__getSongList__(page)
