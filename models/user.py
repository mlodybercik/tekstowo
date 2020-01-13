"""File containing user parse logic"""
from datetime import date
from . import urls
from . import draft
from . import exceptions
from .utils import MONTH, TekstowoSession, SEX


class User:
    """Class for storing info about user
    Local variables:
     - register_date (date)
     - last_login (date)
     - count (str)
     - city (str)
     - county (str)
     - about (str)
     - login (str)
     - name (str)
     - age (int)
     - sex (bool)
     - gg (str)
     - points (int)
     - rank (int)
     - noInvited (int)
     - added ([int, int, int, int])
     - edited ([int, int int])
     - recent ([Song or [str, str]])
     - fanof ([ArtistDraft])
     - invitedUsers ([UserDraft])
     - favSongs ([Song])
    Local methods:
     - getLyrics(self)
     - getTranslations(self)
     - getVideoclips(self)
     - getSoundtracks(self)
     - getInvited(self)
    """

    __slots__ = ["session", "registerDate", "lastLogin", "count", "city", "about",
                 "login", "name", "age", "sex", "gg", "points", "rank",
                 "noInvited", "added", "edited", "recent", "fanof",
                 "invitedUsers", "favSongs", "county"]

    def __init__(self, url, session=None):
        if not isinstance(session, TekstowoSession):
            raise exceptions.TekstowoBadObject("Passed invalid object.")
        else:
            self.session = session
        # this will rise TekstowoBadSite if name is not valid
        page = self.session.get(url).findAll("div", "right-column")[0]

        self.registerDate, self.lastLogin, self.county, \
        self.city, self.about = self.__getDesc__(page)

        self.login, self.name, self.age, self.sex, self.gg, self.points, \
        self.rank, self.noInvited, self.added, self.edited = self.__getStats__(page) # pylint: disable=C0103

        self.recent = self.__getRecent__(page)
        self.fanof = self.__getFanOf__(page)
        self.invitedUsers = self.__getInvited__(page)
        self.favSongs = self.__getFavsongs__(page)

    @classmethod
    def fromLogin(cls, login, session=None):
        """Get user using his login"""
        return cls(urls.PROFILE.format(login), session)


    def __getDesc__(self, page):
        desc = [i.strip() for i in page.findAll("div", "opis")[0].extract().strings]
        registerDateRaw = desc[0][13:-3].split(" ")
        registerDate = date(int(registerDateRaw[2]), MONTH[registerDateRaw[1]],
                            int(registerDateRaw[0]))
        lastLoginRaw = desc[1][21:-3].split(" ")
        lastLogin = date(int(lastLoginRaw[2]), MONTH[lastLoginRaw[1]],
                         int(lastLoginRaw[0]))
        county = desc[2][13:]
        city = desc[3][13:]
        about = desc[7]
        return (registerDate, lastLogin, county, city, about)

    def __getStats__(self, page):
        offset = 0
        page = page.findAll("div", "user-info")[0]
        desc = [i.strip() for i in page.strings]
        login = desc[4][7:]
        name = desc[6]
        if name[:6] == "Wiek: ":
            offset -= 1
            name = ""
        age = int(desc[7 + offset][6:])
        gender = SEX[desc[8+offset][6:]]
        if desc[10 + offset] == "brak":
            gg = -1 # pylint: disable=C0103
        else:
            gg = int(desc[10 + offset]) # pylint: disable=C0103
        if "napisz >" not in desc:
            offset += -3
        points = int(desc[17 + offset])
        # ah yes, site doesnt't seem to be working as it should sometimes
        # rankno is broken, on some profiles it wont even show.
        try:
            rankno = int(desc[-22])
        except ValueError:
            rankno = -1
        invited = int(desc[-19])
        added = (int(desc[-16]), int(desc[-14]), int(desc[-12]), int(desc[-10]))
        edited = (int(desc[-7]), int(desc[-5]), int(desc[-3]))
        return (login, name, age, gender, gg, points, rankno, invited, added, edited)

    def __getRecent__(self, page):
        if not (self.added[0] or self.added[1] or self.added[2] or self.added[3]):
            return []
        recent = []
        for i in page.find_all("div", "box-przeboje"):
            try:
                recent.append(draft.Song(i.a.get("title"), i.a.get("href"), self.session))
            except AttributeError:
                recent.append(list(i.children)[2].strip())
            if "no-bg" in i.get("class"):
                i.extract()
                break
            i.extract()
        return recent

    def __getFanOf__(self, page):
        fanof = []
        page = page.findAll("div", "box-big")[0]
        for i in page.find_all("div", "wykonawca"):
            fanof.append(draft.ArtistDraft(i.a.get("title"), i.a.get("href"), self.session))
        page.extract()
        return fanof

    def __getInvited__(self, page):
        # is this some unfunny *joke*?
        # users invited are displayed as wykonawca class
        # ugh, this site is such a mess
        # failsafe VVV
        if not self.noInvited:
            return []
        invited = []
        page = page.findAll("div", "box-big")[0]
        for i in page.find_all("div", "wykonawca"):
            invited.append(draft.UserDraft(i.text.strip(), i.a.get("href"), self.session))
        page.extract()
        return invited

    def __getFavsongs__(self, page):
        fav = []
        for i in page.find_all("div", "box-przeboje"):
            fav.append(draft.Song(i.a.get("title"), i.a.get("href"), self.session))
            if"no-bg" in i.get("class"):
                break
        return fav

    def _getAdv(self, url, _class=draft.Song, search="box-przeboje"):
        last = False
        pages = 1
        currentPage = 1
        page = self.session.get(url.format(self.login, 1))
        page = page.findAll("div", "content")[0]
        navigation = page.findAll("div", "padding")
        if navigation == []:
            pages = 1
        else:
            pages = int(navigation[0].findAll("a", "page")[-1].get("title"))
        del navigation
        while not last:
            for i in page.findAll("div", search):
                try:
                    try:
                        title = i.a.get("title")
                        if title is None:
                            title = i.a.img.get("alt")
                        yield _class(title, i.a.get("href"), self.session)
                    except AttributeError:
                        yield _class(i.text.strip(), i.a.get("href"), self.session)
                except AttributeError:
                    yield list(i.children)[2].strip()
            if pages == currentPage:
                last = True
            currentPage += 1
            if not last:
                page = self.session.get(url.format(self.login, currentPage))
                page = page.findAll("div", "content")[0]

            else:
                return
        return

    def getLyrics(self):
        """Create getLyrics generator"""
        return self._getAdv(urls.ADDED_TEXTS_PAGE)

    def getTranslations(self):
        """Create getTranslations generator"""
        return self._getAdv(urls.ADDED_TRANSLATIONS_PAGE)

    def getVideoclips(self):
        """Create getVideoclips generator"""
        return self._getAdv(urls.ADDED_VIDEOCLIPS_PAGE)

    def getSoundtracks(self):
        """Create getSoundtracks generator"""
        return self._getAdv(urls.ADDED_SOUNDTRACKS_PAGE)

    def getInvited(self):
        """Create getInvited generator"""
        return self._getAdv(urls.INVITED_PAGE, draft.UserDraft, "wykonawca")
