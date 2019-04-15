from . import artist
from . import lyrics
from . import utils


class _SearchEntry():
    """Main class containing entries for search class
    Local variables:
     - name (str)
     - url (str) # without tekstowo.pl
    """

    _utils = utils.Utils()

    def __init__(self, name, url):
        self.name = name
        self.url = url


class ArtistEntry(_SearchEntry):
    def getArtistObject(self):
        # F*ck python's static variable inheritance.
        return artist.Artist(_SearchEntry._utils.getWebsite("https://www.tekstowo.pl" + self.url))


class SongEntry(_SearchEntry):
    def getLyricsObject(self):
        return lyrics.Lyrics(_SearchEntry._utils.getWebsite("https://www.tekstowo.pl" + self.url))
