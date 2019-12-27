from . import artist
from . import lyrics
from . import utils
from . import draft
from . import urls


class _SearchEntry():
    """Main class containing entries for search class
    Local variables:
     - name (str)
     - url (str) # without base of url (domain)
    """

    _utils = utils.Utils()

    def __str__(self):
        return self.name

    def __init__(self, name, url):
        self.name = name
        self.url = url


class ArtistEntry(_SearchEntry):

    def __repr__(self):
        return "ArtistEntryObject: {}".format(self.name)

    def _parseArtistURL(self):
        return self.url.split(",")[1].split(".")[0]

    def getArtistObject(self):
        # F*ck python's static variable inheritance.
        return artist.Artist(_SearchEntry._utils.getWebsite(urls.artist.format(self._parseArtistURL())))

    def getAllSongs(self):
        songs = []
        page = self._utils.getWebsite(urls.get_all_songs.format(self._parseArtistURL()))
        list = page.find_all("div", "ranking-lista")[0].find_all("div", "box-przeboje")
        for song_ in list:
            songs.append(draft.Song(song_.find_all("a", "title")[0].get("title"), song_.find_all("a", "title")[0].get("href")))
        return songs


class SongEntry(_SearchEntry):

    def __repr__(self):
        return "SongEntryObject: {}".format(self.name)

    def getLyricsObject(self):
        return lyrics.Lyrics(_SearchEntry._utils.getWebsite(urls.base_w + self.url))
