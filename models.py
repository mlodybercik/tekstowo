from bs4 import BeautifulSoup
import requests
import datetime


class Utils:
    """To add proxies and headers overwrite Utils.proxies and Utils.headers"""
    proxies = {}
    headers = {}

    def getWebsite(self, url):
        """Download page and return it as BeautifulSoup class"""
        RAWpage = requests.get(url, proxies=self.proxies, headers=self.headers)
        try:
            if RAWpage.status_code != 200:
                raise("Status code =! 200")
        except Exception:
            raise("No network connection, bad proxy, or bad URL")
        RAWpage = str(bytes(RAWpage.text, "ISO-8859-1"), "utf-8").strip("\n")
        page = BeautifulSoup(RAWpage, "html5lib")
        return page


class Lyrics:
    """Class for storing song lyrics and some info about them
    local variables:
     - artist (str)
     - songName (str)
     - url (str)
     - hasText (bool)
     - hasTranslation (bool)
     - text (str)
     - translation (str)
     - artistUrl (str)
     - comment count (int)
     - id (int)
     - upVotes (int)
    """

    def __init__(self, page):
        """Initialized with site to parse (lyrics page)"""
        if str(type(page)) != "<class 'bs4.BeautifulSoup'>":
            raise("Passed page is not a BeautifulSoup class")
        self.utils = Utils()
        self.__parse__(page)

    def __str__(self):
        return "{artist}:{song}".format(artist=self.artist, song=self.songName)

    def __repr__(self):
        return "{artist}LyricsObject".format(artist=self.artist)

    def getArtistObject(self):
        """returns artist class"""
        return Artist(self.utils._getWebsite(self.artistUrl))

    def getComments(self, amount=30, startFrom=0):
        """Spaghetti code incoming
        code used to download *amount* of comments starting from *startFrom*
        comment in order with its response

        returns [Comment]"""
        commentList = []
        amount = amount - 1
        start = 0
        while True:  # I shouldn't do that
            site = self.utils.getWebsite("http://www.tekstowo.pl/js,moreComments,S,{},{}".format(self.id, startFrom+start+len(commentList)))
            for comment in site.find_all("div", "komentarz"):
                childs = []
                username = comment.a.get("title")
                content = comment.find_all("div", "p")[0].get_text().strip()
                upVotes = comment.find_all("div", "icons")[0].span.get_text()
                url = comment.find_all("a")[0].get("href")
                id = comment.find_all("div", "p")[0].div.get("id").split("comment-")
                if comment.p.getText().strip() == "Pokaż powiązany komentarz ↓":
                    replies = self.utils.getWebsite("http://www.tekstowo.pl/js,showParent,{}".format(id))
                    for reply in replies.find_all("div", "komentarz "):
                        reply_username = comment.a.get("title")
                        reply_content = comment.find_all("div", "p")[0].get_text().strip()
                        reply_url = comment.find_all("a")[0].get("href")
                        childs.append(Comment(reply_username, reply_content, None, None, reply_url, None))
                commentList.append(Comment(username, content, id, None, upVotes, url, childs))
                if not(len(commentList) <= amount):
                    return commentList
        # Failsafe
        return []

    def __getArtist(self, page):
        """Returns artist name"""
        artist = page.find_all("div", "left-corner")[0].find_all("a", "green")[2].get("title")
        return artist

    def __getSongName(self, page):
        """Returns song name"""
        songname = page.find_all("div", "left-corner")[0].find_all("a", "green")[3].get("title")
        return songname

    def __getUrl(self, page):
        """Returns url of a page"""
        url = page.find_all("meta")
        for meta in url:
            if meta.get("property") == "og:url":
                return meta.get("content")

    def __hasText(self, page):
        """Returns True if song has text"""
        if page.find_all("div", "tekst")[0].find_all("div", "song-text"):
            return True
        else:
            return False

    def __getText(self, page):
        """Returns string with song lyrics"""
        text = page.find_all("div", "song-text")[0].get_text()
        return text[65:-130].lstrip().rstrip()

    def __hasTranslation(self, page):
        """Returns True if there is is translation for a given song"""
        if page.find_all("div", "tlumaczenie")[0].find_all("a", "pokaz-tlumaczenie")[0].get("title") == "Pokaż tłumaczenie":
            return True
        else:
            return False

    def __getTranslation(self, page):
        """Returns text translation for given page"""
        return page.find(id="translation").get_text()[65:-130].lstrip().rstrip()

    def __getArtistUrl(self, page):
        try:
            return "http://www.tekstowo.pl/" + page.find_all("a", "link-wykonawca")[0].get("href")
        except IndexError:
            return None

    def __getID(self, page):
        return int(page.find_all("a", "pokaz-rev")[0].get("song_id"))

    def __getCommentCount(self, page):
        return int(page.find_all("h2", "margint10")[0].getText().strip("Komentarze ():"))

    def __getUpVotes(self, page):
        return int(page.find_all("div", "glosowanie")[0].find_all("span", "rank")[0].getText().strip("(+)"))

    def __parse__(self, page):
        """Uses other functions to parse website for information"""
        self.artist       = self.__getArtist(page)
        self.songName     = self.__getSongName(page)
        self.url          = self.__getUrl(page)
        self.artistUrl    = self.__getArtistUrl(page)
        self.id           = self.__getID(page)
        self.commentCount = self.__getCommentCount(page)
        self.upVotes      = self.__getUpVotes(page)

        if self.__hasText(page):
            self.hasText = True
            self.text = self.__getText(page)
            # No need to check for translation if there is not even a normal text
            if self.__hasTranslation(page):
                self.hasTranslation = True
                self.translation = self.__getTranslation(page)
        else:
            self.hasText = False
            self.text = None
            self.hasTranslation = False
            self.translation = None


class Artist:
    """Class for storing artist info and his songs
    local variables:
     - name (str)
     - aboutArtist (str)
     - albums (list or None)
     - amountOfFans (int)
     - songList (list with Song objects)
    """

    def __init__(self, page):
        if str(type(page)) != "<class 'bs4.BeautifulSoup'>":
            raise("Passed page is not a BeautifulSoup class")
            self.utils = Utils()
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
        page = self.utils.getWebsite("http://www.tekstowo.pl/piosenki_artysty,{},alfabetycznie,strona,1.html".format(name))
        amountOfPages = int(page.find_all("div", "padding")[0].find_all("a", "page")[-2].get("title"))
        for pagenumber in range(amountOfPages+1):
            list = page.find_all("div", "ranking-lista")[0].find_all("div", "box-przeboje")
            for song in list:
                songs.append(Song(song.find_all("a", "title")[0].get("title"), song.find_all("a", "title")[0].get("href")))
            page = self.utils.getWebsite("http://www.tekstowo.pl/piosenki_artysty,{},alfabetycznie,strona,{}.html".format(name, pagenumber))
        return songs

    def __parse__(self, page):
        self.name           = self.__getName(page)
        self.aboutArtist    = self.__getAboutArtist(page)
        self.albums         = self.__getAlbums(page)
        self.amountOfFans   = self.__getAmountOfFans(page)
        self.songList       = self.__getSongList(page)


class Song:
    """Song class containing title of the song and its url."""

    def __init__(self, title, url):
        self.title = title
        self.url = "http://www.tekstowo.pl" + url

    def __repr__(self):
        return "{title}SongObject".format(title=self.title)

    def __str__(self):
        return "{title}:{url}".format(title=self.title, url=self.url)

    def getLyricsObject(self):
        tmp = Utils()
        return Lyrics(tmp.getWebsite(self.url))


class Comment:
    """Comment class
    local variables:
    - username (str)
    - content (str)
    - id (int)
    - timedate (timedate)
    - upVotes (int)
    - url (str)
    - childComments (list of Comment)"""

    def __init__(self, username, content, id, timedate, upVotes, url, childComments=None):
        self.username = username
        self.timedate = timedate
        self.content = content
        self.upVotes = upVotes
        self.url = url
        self.childComments = childComments


class AccountSite:
    pass


class SearchEntry:
    pass


class RankingEntry:
    pass
