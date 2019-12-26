from . import user
from . import utils
from . import urls


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
