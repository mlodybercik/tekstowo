from . import user
from . import artist
from . import urls
from . import lyrics
from . import utils
from . import exceptions


class _Draft:
    __slots__ = ["title", "url", "session"]
    def __init__(self, title, url, session=None):
        if not isinstance(session, utils.TekstowoSession):
            raise exceptions.TekstowoBadObject("Passed wrong object")
        self.session = session
        self.title = title
        self.url = urls.base_w + url

    def __str__(self):
        return "{title}:{url}".format(title=self.title, url=self.url)


class ArtistDraft(_Draft):
    """Class containing artist info. Note:
        this isn't a Aritst object.

    Local variables:
     - title (str)
     - url (str)

     Local methods:
     - getArtistObject
    """

    __slots__ = ["title", "url", "session"]
    def __repr__(self):
        return "{title}ArtistDraftObject".format(title=self.title)

    def getArtistObject(self):
        return artist.Artist(self.session.get(self.url), self.session)


class Song(_Draft):
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

    __slots__ = ["title", "url", "session"]
    def __repr__(self):
        return "{title}SongObject".format(title=self.title)

    def getLyricsObject(self):
        return lyrics.Lyrics(self.session.get(self.url), self.session)


class UserDraft(_Draft):
    """Class containing user draft. Note:
        this isn't a User object.

    Local variables:
     - title (str)
     - url (str)

     Local methods:
     - getUserObject
    """

    __slots__ = ["title", "url", "session"]
    def __repr__(self):
        return "{title}UserDraftObject".format(title=self.title)

    def getUserObject(self):
        return user.User(self.session.get(self.url), self.session)
