from . import draft
from . import utils
from . import urls
from . import exceptions
from bs4 import BeautifulSoup


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
    _session = None
    _valid_keys = [["a", "albums"],
                   ["s", "songlist", "songs"]]

    def __init__(self, page, session=None):
        if not isinstance(page, BeautifulSoup):
            raise exceptions.TekstowoBadObject("Passed page is not a BeautifulSoup class")
        if not isinstance(session, utils.TekstowoSession):
            raise exceptions.TekstowoBadJar("Passed object is not a TekstowoSession")
        self.session = session
        self.__parse__(page)

    @classmethod
    def from_url(cls, url, session):
        return cls(session.get(url), session)

    def __str__(self):
        return "{}".format(self.name)

    def __repr__(self):
        return "{}ArtistObject".format(self.name)

    def __getitem__(self, key):
        if key.casefold() in self._valid_keys[0]:
            return self.albums
        elif key.casefold() in self._valid_keys[1]:
            return self.songList
        else:
            raise Exception("Given key is not valid {}".format(key))

    def __getName(self, page):
        """Returns artist name"""
        return page.find_all("div", "belka short")[0].strong.get_text()

    def __getAlbums(self, page):
        """Returns [string] with albums"""
        albums = []
        try:
            for album in page.find(id="artist-disc").find_all("p"):
                albums.append(album.b.get_text())
            return albums
        except Exception:
            return []

    def __getAboutArtist(self, page):
        """Returns the about artist section"""
        try:
            return page.find(id="artist-desc").p.get_text()
        except Exception:
            return ""

    def __getAmountOfFans(self, page):
        """Returns amount of "fans" from page"""
        return int(page.find_all("div", "odslon")[0].get_text().strip("Fanów: "))

    def __getSongList(self, page):
        """Returns list of songs"""
        songs = []
        name = page.find_all("div", "left-corner")[0].find_all("a", "green")[3].get("href")[11:-5:]
        page = self.session.get(urls.artist_songs.format(name))
        list = page.find_all("div", "ranking-lista")[0].find_all("div", "box-przeboje")
        for song_ in list:
            a = song_.find_all("a", "title")[0]
            songs.append(draft.Song(a.get("title"), a.get("href"), self.session))
        return songs

    def __parse__(self, page):
        self.name = self.__getName(page)
        self.aboutArtist = self.__getAboutArtist(page)
        self.albums = self.__getAlbums(page)
        self.amountOfFans = self.__getAmountOfFans(page)
        self.songList = self.__getSongList(page)
