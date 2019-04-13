from . import lyrics
from . import utils


class Song:
    """Class containing song info. Note:
        this isn't a Lyrics object, it doesn't
        contain lyrics.
    Local variables:
     - title (str)
     - url (str)
     - albums (list or None)

     Local methods:
     - getLyricsObject
    """
    util = utils.Utils()  # Thank god this is static <3

    def __init__(self, title, url):
        self.title = title
        self.url = "http://www.tekstowo.pl" + url

    def __repr__(self):
        return "{title}SongObject".format(title=self.title)

    def __str__(self):
        return "{title}:{url}".format(title=self.title, url=self.url)

    def getLyricsObject(self):
        return lyrics.Lyrics(self.util.getWebsite(self.url))
