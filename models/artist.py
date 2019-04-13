from . import song
from . import utils


class Artist:
    """Class for storing artist info and his songs.
    Local variables:
     - name (str)
     - aboutArtist (str)
     - albums (list or None)
     - amountOfFans (int)
     - songList (list with Song objects

     Local methods:
     - None
    """
    utils = utils.Utils()

    def __init__(self, page):
        if str(type(page)) != "<class 'bs4.BeautifulSoup'>":
            raise("Passed page is not a BeautifulSoup class")
        self.__parse__(page)

    def __str__(self):
        return "{name}".format(name=self.name)

    def __repr__(self):
        return "{name}ArtistObject".format(name=self.name)

    def __getName(self, page):
        """Returns artist name"""
        return page.find_all("div", "belka short")[0].strong.get_text()

    def __getAlbums(self, page):
        """Returns [string] with albums"""
        albums = []
        try:
            for album in page.find(id="artist-disc").find_all("p"):
                albums.append(album.b.get_text())
            return albums
        except Exception:
            return []

    def __getAboutArtist(self, page):
        """Returns the about artist section"""
        try:
            return page.find(id="artist-desc").p.get_text()
        except Exception:
            return ""

    def __getAmountOfFans(self, page):
        """Returns amount of "fans" from page"""
        return int(page.find_all("div", "odslon")[0].get_text().strip("Fanów: "))

    def __getSongList(self, page):
        """Returns list of songs"""
        songs = []
        name = page.find_all("div", "left-corner")[0].find_all("a", "green")[3].get("href")[11:-5:]
        page = self.utils.getWebsite("http://www.tekstowo.pl/piosenki_artysty,{},alfabetycznie,strona,0.html".format(name))
        list = page.find_all("div", "ranking-lista")[0].find_all("div", "box-przeboje")
        for song_ in list:
            songs.append(song.Song(song_.find_all("a", "title")[0].get("title"), song_.find_all("a", "title")[0].get("href")))
        return songs

    def __parse__(self, page):
        self.name           = self.__getName(page)
        self.aboutArtist    = self.__getAboutArtist(page)
        self.albums         = self.__getAlbums(page)
        self.amountOfFans   = self.__getAmountOfFans(page)
        self.songList       = self.__getSongList(page)
