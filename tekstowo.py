from bs4 import BeautifulSoup
import requests

def main():
    import argparse

    parser = argparse.ArgumentParser(description="CLI tekstowo wrapper.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--getText","-g", help="get song lyrics",nargs=1, type = str, metavar = "URL")
    group.add_argument("--searchArtist","-s", help="search for an artist",nargs=1, type = str, metavar = "name")
    group.add_argument("--getSongs","-a", help="returns all songs of an artist",nargs=1, type = str, metavar = "name")
    group.add_argument("--giveMeAll","-x", help="returns all songs lyrics in one go",nargs=1, type = str, metavar =  "name")
    args = parser.parse_args()
    dir(args)

    tekstowo = Tekstowo()

    if args.getSongs:
        x = tekstowo.getLyricURLs(args.getSongs[0])
        for i in x:
            print(i + ": " + x[i])
        return 0

    elif args.getText:
        print(tekstowo.getText(args.getText[0]))

    elif args.searchArtist:
        x = tekstowo.searchArtist(args.searchArtist[0])
        for i in x:
            print(i + ": " + x[i])

    elif args.giveMeAll:
        urls = tekstowo.getLyricURLs(args.giveMeAll[0])
        for url in urls:
            print(tekstowo.getText(urls[url]))

    else:
        return 0



class Tekstowo:

    headers = {}

    website = {"artistSearch":  """http://www.tekstowo.pl/szukaj,wykonawca,{},strona,{}.html""",
               "website"     :  """http://www.tekstowo.pl{}""",
               "artistSongs" :  """http://www.tekstowo.pl/piosenki_artysty,{},alfabetycznie,strona,{}.html"""}


    def _getMultiPageContent(self, thing, query, page):
        things = {}
        page = self._getWebsite(self.website[thing].format(query,page))
        if thing == "artistSearch":
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

    def searchArtist(self,artistName):
        artists = {}
        page = self._getWebsite(self.website["artistSearch"].format(artistName,1))
        noPages = page.find_all("div","padding")
        if noPages == []:
            return self._getMultiPageContent("artistSearch", artistName, 1)
        else:
            pages = int(noPages[0].find_all("a","page")[1::-1][0].get_text())
            for site in range(1,pages+1):
                artists.update(self._getMultiPageContent("artistSearch",artistName,site))
        return artists

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
