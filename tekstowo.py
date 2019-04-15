import models


class Tekstowo:

    _utils = models.Utils()

    def getText(self, url):
        """Downloads lyrics and some other stuff from site. See models/* for more"""
        page = self._utils.getWebsite(url)
        return models.Lyrics(page)

    def getArtist(self, url):
        page = self._utils.getWebsite(url)
        return models.Artist(page)

    def searchArtist(self, name):
        return models.ArtistSearch(name)

    def searchSong(self, name):
        return models.SongSearch(name)
