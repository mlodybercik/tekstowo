from bs4 import BeautifulSoup
import requests, datetime

class Utils:
    def __init__(self):
        pass
    def getWebsite(self,url):
        """Download page and return it as BeautifulSoup class"""
        RAWpage = requests.get(url)
        try:
            if RAWpage.status_code != 200:
                raise("Status code =! 200")
        except Exception as e:
            raise("No network connection, bad proxy, or bad URL")
        RAWpage = str(bytes(RAWpage.text,"ISO-8859-1"),"utf-8").strip("\n")
        page = BeautifulSoup(RAWpage,"html5lib")
        return page

class Lyrics:
    """Class for storing song lyrics and some info about them
    local variables:
     - artists (str)
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
    def __init__(self,page):
        """Initialized with site to parse (lyrics page)"""
        if str(type(page)) != "<class 'bs4.BeautifulSoup'>":
            raise("Passed page is not a BeautifulSoup class")
        self.__parse__(page)
    def __str__(self):
        return "{artist}:{song}".format(artist=self.artist, song=self.songName)
    def __repr__(eself):
        return "{artist}LyricsObject".format(artist=self.artist)

    def getArtistObject(self):
        return Artist(_getWebsite(self.artistUrl))
    def getComments(self):
        #self.utils = Utils()
        #utils.getWebsite()
        pass

    def __getArtist(self,page):
        """Returns artist name"""
        artist = page.find_all("div","left-corner")[0].find_all("a","green")[2].get("title")
        return artist
    def __getSongName(self,page):
        """Returns song name"""
        songname = page.find_all("div","left-corner")[0].find_all("a","green")[3].get("title")
        return songname
    def __getUrl(self,page):
        """Returns url of a page"""
        url = page.find_all("meta")
        for meta in url:
            if meta.get("property") == "og:url":
                return meta.get("content")
    def __hasText(self,page):
        """Returns True if song has text"""
        if page.find_all("div","tekst")[0].find_all("div","song-text"):
            return True
        else:
            return False
    def __getText(self,page):
        """Returns string with song lyrics"""
        text = page.find_all("div","song-text")[0].get_text()
        return text[65:-130].lstrip().rstrip()
    def __hasTranslation(self,page):
        """Returns True if there is is translation for a given song"""
        if page.find_all("div","tlumaczenie")[0].find_all("a","pokaz-tlumaczenie")[0].get("title") == "Pokaż tłumaczenie":
            return True
        else:
            return False
    def __getTranslation(self,page):
        """Returns text translation for given page"""
        return page.find(id="translation").get_text()[65:-130].lstrip().rstrip()
    def __getArtistUrl(self,page):
        try:
            return page.find_all("div","belka short")[0].a.get("href")
        except IndexError as e:
            return None
    def __getID(self,page):
        return int(page.find_all("a","pokaz-rev")[0].get("song_id"))
    def __getCommentCount(self,page):
        return int(page.find_all("h2","margint10")[0].getText().strip("Komentarze ():"))
    def __getUpVotes(self,page):
        return int(page.find_all("div","glosowanie")[0].find_all("span","rank")[0].strip("(+)"))

    def __parse__(self,page):
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
            #No need to check for translation if there is not even a normal text
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
    def __init__(self,page):
        self.utils = Utils()
        if str(type(page)) != "<class 'bs4.BeautifulSoup'>":
            raise("Passed page is not a BeautifulSoup class")
        self.__parse__(page)
    def __str__(self):
        return "{name}".format(name=self.name)
    def __repr__(self):
        return "{name}ArtistObject".format(name=self.name)

    def __getName(self,page):
        return page.find_all("div","belka short")[0].strong.get_text()
    def __getAlbums(self,page):
        albums = []
        try:
            for album in page.find(id="artist-disc").find_all("p"):
                albums.append(album.b.get_text())
            return albums
        except Exception as e:
            return []
    def __getAboutArtist(self,page):
        try:
            return page.find(id="artist-desc").p.get_text()
        except Exception as e:
            return ""
    def __getAmountOfFans(self,page):
        return int(page.find_all("div","odslon")[0].get_text().strip("Fanów: "))
    def __getSongList(self,page):
        songs = []
        name = page.find_all("div","left-corner")[0].find_all("a","green")[3].get("href")[11:-5:]
        page = self.utils.getWebsite("http://www.tekstowo.pl/piosenki_artysty,{},alfabetycznie,strona,1.html".format(name))
        amountOfPages = int(page.find_all("div","padding")[0].find_all("a","page")[-2].get("title"))
        for pagenumber in range(amountOfPages+1):
            list = page.find_all("div","ranking-lista")[0].find_all("div","box-przeboje")
            for song in list:
                songs.append(Song(song.find_all("a","title")[0].get("title"),song.find_all("a","title")[0].get("href")))
            page = self.utils.getWebsite("http://www.tekstowo.pl/piosenki_artysty,{},alfabetycznie,strona,{}.html".format(name,pagenumber))
        return songs

    def __parse__(self,page):
        self.name = self.__getName(page)
        self.aboutArtist = self.__getAboutArtist(page)
        self.albums = self.__getAlbums(page)
        self.amountOfFans = self.__getAmountOfFans(page)
        self.songList = self.__getSongList(page)

class Song:
    def __init__(self,title,url):
        self.title = title
        self.url = "http://www.tekstowo.pl" + url
    def __repr__(self):
        return "{title}SongObject".format(title=self.title)
    def __str__(self):
        return "{title}:{url}".format(title=self.title,url=self.url)

    def getLyricsObject(self):
        self.utils = Utils()
        return Lyrics(self.utils.getWebsite(self.url))

class Comment:
    def __init__(self,username,timedate,content,upVotes,url,childComments=None):
        self.username = username
        self.timedate = timedate
        self.content = content
        self.upVotes = upVotes
        self.username = username
        self.timedate = timedate
        self.content = content
        self.upVotes = upVotes
        self.url = url
        self.childComment = childsComment

    def getAccount(self):
        return self.url

class AccountSite:
    pass

class SearchEntry:
    pass

class RankingEntry:
    pass
