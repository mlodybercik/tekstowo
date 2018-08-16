from bs4 import BeautifulSoup
import requests

def main():
    import argparse

    parser = argparse.ArgumentParser(description="CLI tekstowo wrapper.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-g", help="get song lyrics [URL]", action = "store_true")
    group.add_argument("-a", help="returns all songs of an artist [name]", action = "store_true")
    group.add_argument("-s", help="search for an n amount of things", type = str, action = "store", metavar="type", choices = ["artist","song"])
    group.add_argument("-i", help="get info from the website [URL]", action = "store_true")
    group.add_argument("-x", help="returns all songs lyrics in one go [name]", action = "store_true")
    parser.add_argument("name_url", help="of an artist or song")
    parser.add_argument("amount", help="of displayed results", default=10, nargs="?")

    args = parser.parse_args()
    def _webStr(stri):
        r = ""
        tc = {" ":"_"}
        for i in stri:
            if i in tc:
                r += tc[i]
            else:
                r += i
        return r

    tekstowo = Tekstowo(headers=None)

    if args.g:
        if args.name_url[0] != "/":
            print("ERROR: url invalid")
            return -1
        print(tekstowo.getText(args.name_url))
        return 0

    elif args.a:
        x = tekstowo.getLyricURLs(_webStr(args.name_url))
        for i in x:
            print(i + ": " + x[i])
        return 0

    elif args.s:
        if args.s == "artist":
            x = tekstowo.searchArtist(_webStr(args.name_url),int(args.amount))
        if args.s == "song":
            x = tekstowo.searchSong(_webStr(args.name_url),int(args.amount))

        for i in x:
            print(i + ": " + x[i])
        return 0

    elif args.i:
        x = tekstowo.getSongInfo(args.name_url)
        for i in x:
            print(str(i) + ": " + str(x[i]))
        return 0

    elif args.x:
        urls = tekstowo.getLyricURLs(_webStr(args.name_url))
        for url in urls:
            print(tekstowo.getText(urls[url]))
        return 0

class Tekstowo:
    """
    Class for interacting with polish site tekstowo.pl
    """

    ranking = {
                "top"   :"",
                "12m"   :"rok",
                "6m"    :"6-miesiecy",
                "3m"    :"3-miesiace",
                "m"     :"miesiac"
    }

    website = {
               "artistSearch"   :   """http://www.tekstowo.pl/szukaj,wykonawca,{},strona,{}.html""",
               "songSearch"     :   """http://www.tekstowo.pl/szukaj,wykonawca,,tytul,{},strona,{}.html""",
               "website"        :   """http://www.tekstowo.pl{}""",
               "artistSongs"    :   """http://www.tekstowo.pl/piosenki_artysty,{},alfabetycznie,strona,{}.html""",
               "ranking"        :   """http://www.tekstowo.pl/rankingi,{},strona,{}.html""",
               "moreComments"   :   """http://www.tekstowo.pl/js,moreComments,S,{},{}"""
    }

    _current = None
    _prevURL = ""

    def __init__(self,headers={},proxies={}):
        """Initialization of tekstowo class, you can supply requests headers"""
        self.headers = headers
        self.proxies = proxies

    def _getMultiPageContent(self, thing, query, page):
        """Returns dict with a URLs taken from particular site.
        {name : url}
        Used to download data from more than one page
        takes thing and query argument to decide what to search for,
        and page to get content from n'th page"""
        things = {}
        page = self._getWebsite(self.website[thing].format(query,page))

        if thing in ["artistSearch","songSearch"]:
            URLRaw = page.find(id="center").find_all("div","content")[0].find_all("div","box-przeboje")
        else:
            URLRaw = page.find_all("div","ranking-lista")[0].find_all("div","box-przeboje")

        if thing == "ranking":
            for entry in URLRaw:
                title = entry.find_all("a","title")[0].getText()
                url = entry.find_all("a","title")[0].get("href")
                rank = entry.find_all("span","rank")[0].getText()[2:-1]
                if rank == "":
                    rank = "0"
                things[title] = [url,rank]
            return things

        else:
            for entry in URLRaw:
                position = entry.find_all("a","title")[0]
                things[position.get("title")] = position.get("href")
            return things

    def _getWebsite(self,url):
        """Returns beautifulsoup navigable class for further data extraction
        Takes fully assembled url to download page"""
        if url == self._prevURL:
            print("Twice one")
            return self._current
        else:
            site = requests.get(url,headers=self.headers, proxies=self.proxies).text
            site = str(bytes(site,"ISO-8859-1"),"utf-8").strip("\n")
            self._current = BeautifulSoup(site,"html5lib")
            self._prevURL = url
            return self._current

    def getText(self,url):
        """Returns text of a given song. Takes the url of the lyrics
        URL starts with /"""
        try:
            text = self._getWebsite(self.website["website"].format(url)).find_all("div","song-text")[0].get_text()
        except IndexError as e:
            return ""
        return text[65:-130].lstrip().rstrip()

    def searchArtist(self,artistName,amount=10):
        """Returns n amount of search queries for given artist name in dict.
        {name : url}
        Uses _getMultiPageContent to download if amount > 30
        takes html formated name that is without spaces etc."""
        artists = {}
        page = self._getWebsite(self.website["artistSearch"].format(artistName,1))
        noPages = page.find_all("div","padding")
        if noPages == [] or amount < 30:
            artists = self._getMultiPageContent("artistSearch", artistName, 1)
        else:
            pages = int(noPages[0].find_all("a","page")[::-1][:1:][0].get_text())
            for site in range(1,pages+1):
                artists.update(self._getMultiPageContent("artistSearch",artistName,site))
                if len(artists) >= amount:
                    break

        slicedArtists = {}
        for i in artists:
            slicedArtists.update({i:artists[i]})
            if len(slicedArtists) == amount:
                break
        return slicedArtists

    def searchSong(self,name,amount=10):
        """Returns n amount of search queries for given song name in dict.
        {name : url}
        Uses _getMultiPageContent to download if amount > 30
        takes html formatted name that is without spaces etc."""
        songs = {}
        page = self._getWebsite(self.website["songSearch"].format(name,1))
        noPages = page.find_all("div","padding")
        if noPages == [] or amount < 30:
            songs = self._getMultiPageContent("songSearch",name, 1)
        else:
            pages = int(noPages[0].find_all("a","page")[::-1][:1:][0].get_text())
            for site in range(1,pages+1):
                songs.update(self._getMultiPageContent("songSearch",name,site))
                if len(songs) == amount:
                    break

        slicedSongs = {}
        for i in songs:
            slicedSongs.update({i:songs[i]})
            if len(slicedSongs) >= amount:
                break
        return slicedSongs

    def getSongInfo(self,url,comments=False):
        """Returns dict of available information about particular song including comments
        first two entries are views and ID
        { entry : value }
        URL starts with /"""
        info = {}
        page = self._getWebsite(self.website["website"].format(url))
        odslon = page.find_all("div","odslon")[0].getText().replace("Odsłon: ","")
        info.update({"Odslony":int(odslon)})
        ID = page.find_all("a","pokaz-rev")[0].get("song_id")
        info.update({"ID":int(ID)})
        table = page.find_all("div","metric")[0].tbody.find_all("tr")
        for entry in table:
            info.update({entry.th.getText()[:-1:]:entry.td.p.getText()})
        return info

    def getLyricURLs(self, artistName):
        """Returns dict with all songs of an artist
        { name : url }
        Takes url formatted that is without spaces etc."""
        songs = {}
        page = self._getWebsite(self.website["artistSongs"].format(artistName,1))
        noPages = page.find_all("div","padding")
        if noPages == []:
            return self._getMultiPageContent("artistSongs",artistName, 1)
        else:
            pages = int(noPages[0].find_all("a","page")[::-1][:1:][0].get_text())
            for site in range(1,pages+1):
                songs.update(self._getMultiPageContent("artistSongs",artistName,site))
        return songs

    def getRankings(self, time="top", amount=60):
        """Returns dict with n amount of ranking entries
        { name : [url, votes] }
        possible time value in Tekstowo.ranking"""
        if time not in self.ranking:
            raise("Bad time not in ranking")
        ranking = {}
        page = self._getWebsite(self.website["ranking"].format(self.ranking[time],1))
        noPages = page.find_all("div","padding")
        if noPages == [] or (amount < 30 and amount != 0):
            ranking = self._getMultiPageContent("ranking", self.ranking[time], 1)
        else:
            pages = int(noPages[0].find_all("a","page")[::-1][:1:][0].get_text())
            for site in range(1,pages+1):
                ranking.update(self._getMultiPageContent("ranking", self.ranking[time], site))
                if len(ranking) >= amount:
                    break

        slicedRanking = {}
        for i in ranking:
            slicedRanking.update({i:ranking[i]})
            if len(slicedRanking) == amount:
                break
        return slicedRanking

if __name__ == "__main__":
    main()
