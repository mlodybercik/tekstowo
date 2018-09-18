from models import Utils, Lyrics, Artist


class Tekstowo:

    website = {
        "main":   """http://www.tekstowo.pl/{}"""}

    def __init__(self):
        self.utils = Utils()

    def getText(self, url):
        """Downloads lyrics and some other stuff from site. See models.py for more"""
        page = self.utils.getWebsite(url)
        return Lyrics(page)

    def getArtist(self, url):
        page = self.utils.getWebsite(url)
        return Artist(page)
