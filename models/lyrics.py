from . import artist
from . import comment
from . import utils
from . import urls
from . import exceptions
from bs4 import BeautifulSoup


class Lyrics:
    """Class for storing song lyrics and some info about them.
    Local variables:
     - artist (str)
     - songName (str)
     - url (str)
     - hasText (bool)
     - hasTranslation (bool)
     - text (str) # can be very long
     - translation (str)
     - artistUrl (str)
     - commentCount (int)
     - id (int)
     - upVotes (int)

    Local methods: # rather self explanatory
     - getComments(self, amount=30, startFrom=0)
     - getArtistObject(self)
     - rankSongUp(self)
     - rankSongDown(self)
    """

    __slots__ = ["session", "artist", "songName", "url", "hasText", "hasTranslation",
                 "text", "translation", "artistUrl", "commentCount", "id", "upVotes"]

    def __init__(self, page, session=None):
        if not isinstance(page, BeautifulSoup):
            raise exceptions.TekstowoBadObject("Passed page is not a BeautifulSoup class")
        if not isinstance(session, utils.TekstowoSession):
            raise exceptions.TekstowoBadJar("Passed object is not a TekstowoSession")
        self.session = session
        self.__parse__(page)

    @classmethod
    def from_url(cls, url, session):
        return cls(session.get(url), session)

    def __str__(self):
        return "{artist}:{song}".format(artist=self.artist, song=self.songName)

    def __repr__(self):
        return "{artist}LyricsObject".format(artist=self.artist)

    def __int__(self):
        return self.id

    def __getArtist(self, page):
        """Returns artist name"""
        try:
            artist_ = page.find_all("div", "left-corner")[0].find_all("a", "green")[2].get("title")
            return artist_
        except Exception:
            return None

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
        return page.find(id="translation").get_text()[:-130].lstrip().rstrip()

    def __getArtistUrl(self, page):
        try:
            return urls.base_w + page.find_all("a", "link-wykonawca")[0].get("href")
        except IndexError:
            return None

    def __getID(self, page):
        try:
            return int(page.find_all("a", "pokaz-rev")[0].get("song_id"))
        except Exception:
            return -1

    def __getCommentCount(self, page):
        try:
            return int(page.find_all("h2", "margint10")[0].getText().strip("Komentarze ():"))
        except Exception:
            return -1

    def __getUpVotes(self, page):
        try:
            return int(page.find_all("div", "glosowanie")[0].find_all("span", "rank")[0].getText().strip("(+)"))
        except Exception:
            return -1

    def __parse__(self, page):
        """Uses other functions to parse website for information"""
        self.artist = self.__getArtist(page)
        self.songName = self.__getSongName(page)
        self.url = self.__getUrl(page)
        self.artistUrl = self.__getArtistUrl(page)
        self.id = self.__getID(page)
        self.commentCount = self.__getCommentCount(page)
        self.upVotes = self.__getUpVotes(page)

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

    def getComments(self, amount=30, startFrom=0):
        """Spaghetti code incoming...
        code used to download *amount* of comments starting from *startFrom*
        comment in order with its replies

        returns [Comment]"""

        if self.commentCount == 0:
            return []

        if amount > self.commentCount:
            amount = self.commentCount
        elif amount == 0:
            amount = self.commentCount

        start = 0
        commentList = []
        while len(commentList) < amount:
            site = self.session.get(urls.get_coments.format(self.id, startFrom+start+len(commentList)))
            for comment_ in site.find_all("div", "komentarz"):
                try:
                    childs = []
                    replyID = None
                    # this looks awful
                    username = comment_.a.get("title")
                    content = comment_.find_all("div", "p")[0].get_text().strip()
                    upVotes = comment_.find_all("div", "icons")[0].span.get_text()[1:-1]
                    url = comment_.find_all("a")[0].get("href")
                    time = comment_.find_all("div", "bar")[0].contents[2].split()
                    id_ = comment_.find_all("div", "p")[0].div.get("id")[8:]
                    if "↓" in comment_.p.getText().strip():
                        replyID = comment_.find_all("p")[0].a.get("onclick")[19:-1]
                        replies = self.session.get(urls.get_replies.format(replyID))
                        for reply in replies.find_all("div", "komentarz "):
                            reply_username = reply.a.get("title")
                            reply_content = reply.find_all("div", "p")[0].get_text().strip()
                            reply_url = reply.find_all("a")[0].get("href")
                            reply_time = reply.find_all("div", "bar")[0].contents[2].split()
                            reply_upVotes = reply.find_all("div", "icons")[0].span.get_text()[1:-1]
                            childs.append(comment.Comment(reply_username, reply_content, None, reply_time, reply_upVotes, reply_url, None))
                    if replyID is not None:
                        commentList.append(comment.Comment(username, content, id_, time, upVotes, url, replyID, childs))
                    else:
                        commentList.append(comment.Comment(username, content, id_, time, upVotes, url, None, childs))
                except Exception:
                    commentList.append(comment.Comment("Exception", "Exception", 0, 0, 0, "Exception"))
                finally:
                    if not(len(commentList) <= amount):
                        return commentList
                    if len(commentList) >= self.commentCount:
                        return commentList

        # Failsafe
        return []

    def getArtistObject(self):
        """returns artist class"""
        return artist.Artist(self.session.get(self.artistUrl), self.session)

    def _rankSong(self, action):
        """Rank song. Returns 1 when succesfully voted, returns 2 when already voted.
        Raises TekstowoNotLoggedIn when session is bad."""
        if action not in ["Up", "Down"]:
            raise exceptions.TekstowoBadObject(f"{action} is not a valid action")
        if(self.session.islogged):
            if(action == "Up"):
                ret = self.session.raw_get(urls.rank_up.format(self.id))
            else:
                ret = self.session.raw_get(urls.rank_down.format(self.id))
            if ret == '"voted_ip"':
                return 2
            elif ret == '"voted"':
                return 2
            elif ret == 'true':
                return 1
            elif ret == '"not logged"':
                raise exceptions.TekstowoNotLoggedIn("Bad session. Site returned not logged in.")
            else:
                return ret

    def rankSongUp(self):
        """Vote up on song. Go see _rankSong for info."""
        return self._rankSong("Up")

    def rankSongDown(self):
        """Vote down on song. Go see _rankSong for info."""
        return self._rankSong("Down")
