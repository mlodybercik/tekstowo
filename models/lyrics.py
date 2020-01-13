"""Main file holding logic for parsing lyrics."""
from bs4 import BeautifulSoup
from . import artist
from . import comment
from . import utils
from . import urls
from . import exceptions


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
    def fromUrl(cls, url, session):
        """Get text from given url"""
        return cls(session.get(url), session)

    def __str__(self):
        return "{artist}:{song}".format(artist=self.artist, song=self.songName)

    def __repr__(self):
        return "{artist}LyricsObject".format(artist=self.artist)

    def __int__(self):
        return self.id

    @exceptions.catchAndReturn(bool)
    def __getArtist__(self, page):
        """Returns artist name"""
        return page.find_all("div", "left-corner")[0].find_all("a", "green")[2].get("title")


    def __getSongName__(self, page):
        """Returns song name"""
        songname = page.find_all("div", "left-corner")[0].find_all("a", "green")[3].get("title")
        return songname

    def __getUrl__(self, page):
        """Returns url of a page"""
        url = page.find_all("meta")
        for meta in url:
            if meta.get("property") == "og:url":
                return meta.get("content")

    def __hasText__(self, page):
        """Returns True if song has text"""
        if page.find_all("div", "tekst")[0].find_all("div", "song-text"):
            return True
        else:
            return False

    def __getText__(self, page):
        """Returns string with song lyrics"""
        text = page.find_all("div", "song-text")[0].get_text()
        return text[65:-130].lstrip().rstrip()

    def __hasTranslation__(self, page):
        """Returns True if there is is translation for a given song"""
        if page.find_all("div", "tlumaczenie")[0]\
            .find_all("a", "pokaz-tlumaczenie")[0]\
            .get("title") == "Pokaż tłumaczenie":
            return True
        else:
            return False

    def __getTranslation__(self, page):
        """Returns text translation for given page"""
        return page.find(id="translation").get_text()[:-130].lstrip().rstrip()

    @exceptions.catchAndReturn(bool)
    def __getArtistUrl__(self, page):
        return urls.BASE_W + page.find_all("a", "link-wykonawca")[0].get("href")

    @exceptions.catchAndReturn(bool)
    def __getID__(self, page):
        return int(page.find_all("a", "pokaz-rev")[0].get("song_id"))

    @exceptions.catchAndReturn(bool)
    def __getCommentCount__(self, page):
        return int(page.find_all("h2", "margint10")[0].getText().strip("Komentarze ():"))

    @exceptions.catchAndReturn(bool)
    def __getUpVotes__(self, page):
        return int(page.find_all("div", "glosowanie")[0]\
                   .find_all("span", "rank")[0]\
                   .getText().strip("(+)"))

    def __parse__(self, page):
        """Uses other functions to parse website for information"""
        self.artist = self.__getArtist__(page)
        self.songName = self.__getSongName__(page)
        self.url = self.__getUrl__(page)
        self.artistUrl = self.__getArtistUrl__(page)
        self.id = self.__getID__(page) # pylint: disable=C0103
        self.commentCount = self.__getCommentCount__(page)
        self.upVotes = self.__getUpVotes__(page)

        if self.__hasText__(page):
            self.hasText = True
            self.text = self.__getText__(page)
            # No need to check for translation if there is not even a normal text
            if self.__hasTranslation__(page):
                self.hasTranslation = True
                self.translation = self.__getTranslation__(page)
            else:
                self.hasTranslation = False
                self.translation = None
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

        if startFrom > self.commentCount:
            return []

        start = 0
        commentList = []
        done = False
        while (len(commentList) < amount) and not done:
            site = self.session.get(urls.GET_COMMENTS.format(self.id,
                                                             startFrom+start+len(commentList)))
            for _comment in site.find_all("div", "komentarz"):
                try:
                    childs = []
                    replyID = None
                    # this looks awful
                    username = _comment.a.get("title")
                    content = _comment.find_all("div", "p")[0].get_text().strip()
                    upVotes = _comment.find_all("div", "icons")[0].span.get_text()[1:-1]
                    url = _comment.find_all("a")[0].get("href")
                    time = _comment.find_all("div", "bar")[0].contents[2].split()
                    id_ = _comment.find_all("div", "p")[0].div.get("id")[8:] # pylint: disable=C0103
                    if "↓" in _comment.p.getText().strip():
                        replyID = _comment.find_all("p")[0].a.get("onclick")[19:-1]
                        replies = self.session.get(urls.GET_REPLIES.format(replyID))
                        for reply in replies.find_all("div", "komentarz "):
                            replyUsername = reply.a.get("title")
                            replyContent = reply.find_all("div", "p")[0].get_text().strip()
                            replyUrl = reply.find_all("a")[0].get("href")
                            replyTime = reply.find_all("div", "bar")[0].contents[2].split()
                            replyUpVotes = reply.find_all("div", "icons")[0].span.get_text()[1:-1]
                            childs.append(comment.Comment(replyUsername, replyContent,
                                                          None, replyTime, replyUpVotes,
                                                          replyUrl, None))
                    if replyID is not None:
                        commentList.append(comment.Comment(username, content,
                                                           id_, time, upVotes,
                                                           url, replyID, childs))
                    else:
                        commentList.append(comment.Comment(username, content,
                                                           id_, time, upVotes,
                                                           url, None, childs))
                except Exception: # FIXME: too broad except
                    commentList.append(comment.Comment.empty())
                finally:
                    if not(len(commentList) <= amount) or len(commentList) >= self.commentCount:
                        done = True

        return commentList

    def getArtistObject(self):
        """returns artist class"""
        return artist.Artist(self.session.get(self.artistUrl), self.session)

    def _rankSong(self, action):
        """Rank song. Returns 1 when succesfully voted, returns 2 when already voted.
        Raises TekstowoNotLoggedIn when session is bad."""
        if action not in ["Up", "Down"]:
            raise exceptions.TekstowoBadObject(f"{action} is not a valid action")
        if self.session.islogged:
            if action == "Up":
                ret = self.session.raw_get(urls.RANK_UP.format(self.id))
            else:
                ret = self.session.raw_get(urls.RANK_DOWN.format(self.id))
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
