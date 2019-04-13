import models


class Tekstowo:

    _utils = models.Utils()

    def __init__(self):
        pass

    def getText(self, url):
        """Downloads lyrics and some other stuff from site. See models.py for more"""
        page = self._utils.getWebsite(url)
        return models.Lyrics(page)

    def getArtist(self, url):
        page = self._utils.getWebsite(url)
        return models.Artist(page)
