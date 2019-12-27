from . import utils
from . import urls
from . import draft
from datetime import date


class User:
    "Class for storing info about user"

    # TODO: this is reuse of comment.month
    month = {"stycznia": 1,
             "lutego": 2,
             "marca": 3,
             "kwietnia": 4,
             "maja": 5,
             "czerwca": 6,
             "lipca": 7,
             "sierpnia": 8,
             "września": 9,
             "października": 10,
             "listopada": 11,
             "grudnia": 12}

    # TODO: chnage those names xD
    sex_table = {"Kobieta": 0, "Mężczyzna": 1}

    def __init__(self, login, jar=None):
        if(not jar):
            self.jar = utils.TekstowoSession()
        else:
            self.jar = jar
        # this will rise TekstowoBadSite if name is not valid
        page = self.jar.get(urls.profile.format(login))
        self.login = login
        self.__parse(page)

    def __parse(self, site):
        site = site.findAll("div", "right-column")[0]
        self.register_date, self.last_login, self.county, \
            self.city, self.about = self.__getDesc(site)

        self.name, self.sex, self.gg, self.points, self.rank, \
            self.noInvited, self.added, self.edited = self.__getStats(site)

        self.recent = self.__getRecent(site)
        self.fanof = self.__getFanOf(site)
        self.invitedUsers = self.__getInvited(site)
        self.favSongs = self.__getFavsongs(site)

    def __getDesc(self, page):
        desc = [i.strip() for i in page.findAll("div", "opis")[0].extract().strings]
        register_date_raw = desc[0][13:-3].split(" ")
        register_date = date(int(register_date_raw[2]), self.month[register_date_raw[1]], int(register_date_raw[0]))
        last_login_raw = desc[1][21:-3].split(" ")
        last_login = date(int(last_login_raw[2]), self.month[last_login_raw[1]], int(last_login_raw[0]))
        county = desc[2][13:]
        city = desc[3][13:]
        about = desc[7]
        return (register_date, last_login, county, city, about)

    def __getStats(self, page):
        offset = 0
        page = page.findAll("div", "user-info")[0]
        desc = [i.strip() for i in page.strings]
        name = desc[6]
        if name[:6] == "Wiek: ":
            offset -= 1
            name = ""
        gender = self.sex_table[desc[8+offset][6:]]
        if desc[10 + offset] == "brak":
            gg = -1
        else:
            gg = int(desc[10 + offset])
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
        return (name, gender, gg, points, rankno, invited, added, edited)

    def __getRecent(self, page):
        if(not (self.added[0] or self.added[1] or self.added[2] or self.added[3])):
            return []
        recent = []
        for i in page.find_all("div", "box-przeboje"):
            try:
                recent.append(draft.Song(i.a.get("title"), i.a.get("href")))
            except AttributeError:
                recent.append(list(i.children)[2].strip())
            if("no-bg" in i.get("class")):
                i.extract()
                break
            i.extract()
        return recent

    def __getFanOf(self, page):
        fanof = []
        # is this some unfunny *joke*?
        # users invited are displayed as wykonawca class
        # ugh, this site is such a mess
        # failsafe VVV
        page = page.findAll("div", "box-big")[0]
        for i in page.find_all("div", "wykonawca"):
            fanof.append(draft.ArtistDraft(i.a.get("title"), i.a.get("href")))
        page.extract()
        return fanof

    def __getInvited(self, page):
        if(not self.noInvited):
            return []
        invited = []
        page = page.findAll("div", "box-big")[0]
        for i in page.find_all("div", "wykonawca"):
            invited.append(draft.UserDraft(i.text.strip(), i.a.get("href")))
        page.extract()
        return invited

    def __getFavsongs(self, page):
        fav = []
        for i in page.find_all("div", "box-przeboje"):
            fav.append(draft.Song(i.a.get("title"), i.a.get("href")))
            if("no-bg" in i.get("class")):
                break
        return fav
