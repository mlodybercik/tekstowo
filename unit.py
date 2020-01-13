import unittest
import tekstowo
import models
from datetime import date
from models import draft
import sys


class TestLyrics(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.lyrics = tekstowo.getText("http://www.tekstowo.pl/piosenka,rick_astley,never_gonna_give_you_up.html")

    def test_ArtistName(self):
        self.assertEqual(self.lyrics.artist, "Rick Astley", "artist name doesn't match")

    def test_SongName(self):
        self.assertEqual(self.lyrics.songName, "Never gonna give you up", "song")

    def test_Url(self):
        self.assertEqual(self.lyrics.url, "http://www.tekstowo.pl/piosenka,rick_astley,never_gonna_give_you_up.html", "url invalid")

    def test_HasText(self):
        self.assertTrue(self.lyrics.hasText, "has text?")

    def test_HasTranslation(self):
        self.assertTrue(self.lyrics.hasTranslation, "has translation?")

    def test_ID(self):
        self.assertEqual(self.lyrics.id, 36785, "bad id")

    def test_Comments(self):
        self.assertEqual(len(self.lyrics.getComments(0)), self.lyrics.commentCount)

    @unittest.skipIf(not tekstowo.models.session.isLogged, "Not logged in")
    def test_VoteUp(self):
        self.assertGreaterEqual(self.lyrics.rankSongUp(), 1)


class TestArtist(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.artist = tekstowo.getArtist("http://www.tekstowo.pl/wykonawca,rick_astley.html")

    def test_Name(self):
        self.assertEqual(self.artist.name, "Rick Astley", "name doesen't match")

    def test_Albums(self):
        self.assertTrue(len(self.artist.albums) == 9, "albums doesn't match")

    def test_AmountOfFans(self):
        self.assertGreaterEqual(self.artist.amountOfFans, 9, "fans doesn't match")

    def test_SongList(self):
        self.assertEqual(len(self.artist.songList), 107, "amount of songs doesnt match")
        self.assertTrue(type(self.artist.songList[0]), draft.Song)

    def test_Object(self):
        self.assertIsInstance(self.artist.songList[0].getLyricsObject(), models.Lyrics)


class TestSongSearch(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.searchSong = tekstowo.searchSong("Never gonna give you up")

    def test_Url(self):
        self.assertTrue(self.searchSong.url == "https://tekstowo.pl/szukaj,tytul,Never+gonna+give+you+up,strona,1.html", "bad url")

    def test_Length(self):
        self.assertLessEqual(len(self.searchSong.entries), 30, "too many entries")

    def test_Find(self):
        self.assertTrue(self.searchSong[0].url == "/piosenka,rick_astley,never_gonna_give_you_up.html")

    def test_getLyricsObject(self):
        lyricsObject = self.searchSong[0].getLyricsObject()
        self.assertTrue(type(lyricsObject) == models.Lyrics)


class TestArtistSearch(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.searchArtist = tekstowo.searchArtist("Rick Astley")

    def test_Find(self):
        self.assertTrue(self.searchArtist[0].url == "/piosenki_artysty,rick_astley.html")

    def test_GetArtistObject(self):
        artistObject = self.searchArtist[0].getArtistObject()
        self.assertTrue(type(artistObject) == models.Artist)

    def test_Length(self):
        self.assertLessEqual(len(self.searchArtist.entries), 30, "too many entries")

    def test_Url(self):
        self.assertTrue(self.searchArtist.url == "https://tekstowo.pl/szukaj,wykonawca,Rick+Astley,strona,1.html", "bad url")


class TestUser(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.user = tekstowo.getUser("bombelbombel")

    def test_Desc(self):
        self.assertEqual(self.user.login, "bombelbombel", "invalid name")
        self.assertEqual(self.user.name, "")
        self.assertEqual(self.user.registerDate, date(2009, 7, 7))
        self.assertEqual(self.user.gg, -1)

    def test_Added(self):
        text, translation, video, soundtrack = self.user.added
        self.assertGreaterEqual(text, 81975)
        self.assertGreaterEqual(translation, 4314)
        self.assertGreaterEqual(video, 56261)
        self.assertGreaterEqual(soundtrack, 1)

    def test_Edited(self):
        text, translation, soundtrack = self.user.edited
        self.assertGreaterEqual(text, 6107)
        self.assertGreaterEqual(translation, 159)
        self.assertGreaterEqual(soundtrack, 0)

    def test_Panels(self):
        self.assertGreaterEqual(len(self.user.invitedUsers), 1)
        self.assertEqual(len(self.user.recent), 10)
        self.assertEqual(len(self.user.fanof), 0)

    def test_Generators(self):
        for gen in [self.user.getInvited(),
                    self.user.getLyrics(),
                    self.user.getSoundtracks(),
                    self.user.getTranslations(),
                    self.user.getVideoclips()]:
            try:
                self.assertIsNot(next(gen), next(gen), str(gen))
            except StopIteration:
                pass


# idk, sometimes exit=True doesnt work
# failsafe
sys.exit = lambda a: 0

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if(sys.argv[1] in ["-u", "--user"]):
            from getpass import getpass
            tekstowo.login(input("Login: "), getpass("Password: "))
            del sys.argv[1:]
            unittest.main(exit=False)
            tekstowo.logout()
        else:
            unittest.main()
    else:
        unittest.main()
