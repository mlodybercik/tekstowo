from . import artist
from . import utils
from . import urls
from . import lyrics
from . import user


class ArtistDraft:
    """Class containing artist info. Note:
        this isn't a Aritst object.

    Local variables:
     - title (str)
     - url (str)

     Local methods:
     - getArtistObject
    """
    util = utils.Utils()

    def __init__(self, title, url):
        self.title = title
        self.url = urls.base_w + url

    def __repr__(self):
        return "{title}ArtistDraftObject".format(title=self.title)

    def __str__(self):
        return "{title}:{url}".format(title=self.title, url=self.url)

    def getArtistObject(self):
        return artist.Artist(self.util.getWebsite(self.url))


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
        self.url = urls.base_w + url

    def __repr__(self):
        return "{title}SongObject".format(title=self.title)

    def __str__(self):
        return "{title}:{url}".format(title=self.title, url=self.url)

    def getLyricsObject(self):
        return lyrics.Lyrics(self.util.getWebsite(self.url))


class UserDraft:
    """Class containing user draft. Note:
        this isn't a User object.

    Local variables:
     - name (str)
     - url (str)

     Local methods:
     - getArtistObject
    """
    util = utils.Utils()

    def __init__(self, name, url):
        self.name = name
        self.url = urls.base_w + url

    def __repr__(self):
        return "{title}UserDraftObject".format(title=self.name)

    def __str__(self):
        return "{title}:{url}".format(title=self.name, url=self.url)

    def getUserObject(self):
        return user.User(self.util.getWebsite(self.url))
