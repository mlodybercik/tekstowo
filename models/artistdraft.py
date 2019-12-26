from . import artist
from . import utils
from . import urls


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
