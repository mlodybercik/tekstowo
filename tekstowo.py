from bs4 import BeautifulSoup
import requests

def main():
    import argparse

    parser = argparse.ArgumentParser(description="CLI tekstowo wrapper.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--getText","-g", help="get song lyrics",nargs=1, type = str, metavar = "/URL.html")
    group.add_argument("--searchArtist","-s", help="search for an n amount of artists",nargs=2, type = str, metavar = "name n")
    group.add_argument("--searchSong","-S",help="search for n amount of songs", nargs=2, type = str, metavar = "artist n")
    group.add_argument("--getSongs","-a", help="returns all songs of an artist", nargs=1, type = str, metavar = "song")
    group.add_argument("--giveMeAll","-x", help="returns all songs lyrics in one go",nargs=1, type = str, metavar =  "artist")

    args = parser.parse_args()
    dir(args)

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

    if args.getText:
        print(tekstowo.getText(args.getText[0]))
        return 0


    elif args.searchArtist:
        x = tekstowo.searchArtist(_webStr(args.searchArtist[0]),int(args.searchArtist[1]))
        for i in x:
            print(i + ": " + x[i])
        return 0

    elif args.searchSong:
        x = tekstowo.searchSong(_webStr(args.searchSong[0]),int(args.searchSong[1]))
        for i in x:
            print(i + ": " + x[i])
        return 0

    elif args.getSongs:
        x = tekstowo.getLyricURLs(_webStr(args.getSongs[0]))
        for i in x:
            print(i + ": " + x[i])
        return 0

    elif args.giveMeAll:
        urls = tekstowo.getLyricURLs(_webStr(args.giveMeAll[0]))
        for url in urls:
            print(tekstowo.getText(urls[url]))
        return 0

class Tekstowo:

    headers = {}

    website = {"artistSearch"   :  """http://www.tekstowo.pl/szukaj,wykonawca,{},strona,{}.html""",
               "songSearch"     :  """http://www.tekstowo.pl/szukaj,wykonawca,,tytul,{},strona,{}.html""",
               "website"        :  """http://www.tekstowo.pl{}""",
               "artistSongs"    :  """http://www.tekstowo.pl/piosenki_artysty,{},alfabetycznie,strona,{}.html"""}

    def __init__(self,headers):
        self.headers = headers

    def _getMultiPageContent(self, thing, query, page):
        things = {}
        page = self._getWebsite(self.website[thing].format(query,page))
        if thing in ["artistSearch","songSearch"]:
            URLRaw = page.find(id="center").find_all("div","content")[0].find_all("div","box-przeboje")
        else:
            URLRaw = page.find_all("div","ranking-lista")[0].find_all("div","box-przeboje")
        for entry in URLRaw:
            position = entry.find_all("a","title")[0]
            things[position.get("title")] = position.get("href")
        return things

    def _getWebsite(self,url):
        site = requests.get(url,headers=self.headers).text
        site = str(bytes(site,"ISO-8859-1"),"utf-8").strip("\n")
        return BeautifulSoup(site,"html.parser")


    def getText(self,url):
        text = self._getWebsite(self.website["website"].format(url)).find_all("div","song-text")[0].get_text()
        return text[40:-62]

    def searchArtist(self,artistName,amount=10):
        artists = {}
        page = self._getWebsite(self.website["artistSearch"].format(artistName,1))
        noPages = page.find_all("div","padding")
        if noPages == [] or amount < 30:
            artists = self._getMultiPageContent("artistSearch", artistName, 1)
        else:
            pages = int(noPages[0].find_all("a","page")[1::-1][0].get_text())
            for site in range(1,pages+1):
                artists.update(self._getMultiPageContent("artistSearch",artistName,site))
                if len(artists) < amount:
                    break
        slicedArtists = {}
        for i in artists:
            slicedArtists.update({i:artists[i]})
            if len(slicedArtists) == amount:
                break
        return slicedSongs

    def searchSong(self,name,amount=10):
        songs = {}
        page = self._getWebsite(self.website["songSearch"].format(name,1))
        noPages = page.find_all("div","padding")
        if noPages == [] or amount < 30:
            songs = self._getMultiPageContent("songSearch",name, 1)
        else:
            pages = int(noPages[0].find_all("a","page")[1::-1][0].get_text())
            for site in range(1,pages+1):
                songs.update(self._getMultiPageContent("songSearch",name,site))
                if len(songs) < amount:
                    break
        slicedSongs = {}
        for i in songs:
            slicedSongs.update({i:songs[i]})
            if len(slicedSongs) == amount:
                break
        return slicedSongs

    def getLyricURLs(self, artistName):
        songs = {}
        page = self._getWebsite(self.website["artistSongs"].format(artistName,1))
        noPages = page.find_all("div","padding")
        if noPages == []:
            return self._getMultiPageContent("artistSongs",artistName, 1)
        else:
            pages = int(noPages[0].find_all("a","page")[1::-1][0].get_text())
            for site in range(1,pages+1):
                songs.update(self._getMultiPageContent("artistSongs",artistName,site))
        return songs

if __name__ == "__main__":
    main()
