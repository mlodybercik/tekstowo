"""SearchEntry logic, Search object has array of SearchEntries for Artist or Song."""
from . import artist
from . import lyrics
from . import draft
from . import urls
from . import exceptions
from . import utils


class _SearchEntry:
    """Main class containing entries for search class
    Local variables:
     - name (str)
     - url (str) # without base of url (domain)
    """

    def __str__(self):
        return self.name

    def __init__(self, name, url, session=None):
        if not isinstance(session, utils.TekstowoSession):
            raise exceptions.TekstowoBadObject("Passed wrong object.")
        self.session = session
        self.name = name
        self.url = url


class ArtistEntry(_SearchEntry):
    """Class containing entries for search class
    Local variables:
     - name (str)
     - url (str) # without base of url (domain)
    """
    __slots__ = ["name", "url", "session"]

    def __repr__(self):
        return "ArtistEntryObject: {}".format(self.name)

    def _parseArtistURL(self):
        return self.url.split(",")[1].split(".")[0]

    def getArtistObject(self):
        """Create Artist object from entry."""
        return artist.Artist(self.session.get(urls.ARTIST.format(self._parseArtistURL())),
                             self.session)

    def getAllSongs(self):
        """Shortcut to get all songs of a given artist from search"""
        songs = []
        page = self.session.get(urls.GET_ALL_SONGS.format(self._parseArtistURL()))
        _list = page.find_all("div", "ranking-lista")[0].find_all("div", "box-przeboje")
        for _song in _list:
            songs.append(draft.Song(_song.find_all("a", "title")[0].get("title"),
                                    _song.find_all("a", "title")[0].get("href"), self.session))
        return songs


class SongEntry(_SearchEntry):
    """Class containing entries for search class
    Local variables:
     - name (str)
     - url (str) # without base of url (domain)
    """
    __slots__ = ["name", "url", "session"]

    def __repr__(self):
        return "SongEntryObject: {}".format(self.name)

    def getLyricsObject(self):
        """Create Lyrics object from entry."""
        return lyrics.Lyrics(self.session.get(urls.BASE_W + self.url), self.session)
