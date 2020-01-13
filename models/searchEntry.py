from . import artist
from . import lyrics
from . import draft
from . import urls
from . import exceptions
from . import utils


class _SearchEntry():
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
    __slots__ = ["name", "url", "session"]

    def __repr__(self):
        return "ArtistEntryObject: {}".format(self.name)

    def _parseArtistURL(self):
        return self.url.split(",")[1].split(".")[0]

    def getArtistObject(self):
        return artist.Artist(self.session.get(urls.artist.format(self._parseArtistURL())), self.session)

    def getAllSongs(self):
        songs = []
        page = self.session.get(urls.get_all_songs.format(self._parseArtistURL()))
        list_ = page.find_all("div", "ranking-lista")[0].find_all("div", "box-przeboje")
        for song_ in list_:
            songs.append(draft.Song(song_.find_all("a", "title")[0].get("title"), song_.find_all("a", "title")[0].get("href"), self.session))
        return songs


class SongEntry(_SearchEntry):
    __slots__ = ["name", "url", "session"]

    def __repr__(self):
        return "SongEntryObject: {}".format(self.name)

    def getLyricsObject(self):
        return lyrics.Lyrics(self.session.get(urls.base_w + self.url), self.session)
