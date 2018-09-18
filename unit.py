import unittest
from tekstowo import *


class TestLyrics(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        x = Utils()
        y = x.getWebsite("http://www.tekstowo.pl/piosenka,rick_astley,never_gonna_give_you_up.html")
        self.lyrics = Lyrics(y)

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

    def test_id(self):
        self.assertEqual(self.lyrics.id, 36785, "bad id")


class TestArtist(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.utils = Utils()
        self.artist = Artist(self.utils.getWebsite("http://www.tekstowo.pl/wykonawca,rick_astley.html"))

    def test_Name(self):
        self.assertEqual(self.artist.name, "Rick Astley", "name doesen't match")

    def test_Albums(self):
        self.assertTrue(len(self.artist.albums) == 9, "albums doesn't match")

    def test_AmountOfFans(self):
        self.assertGreaterEqual(self.artist.amountOfFans, 9, "fans doesn't match")

    def test_songList(self):
        self.assertEqual(len(self.artist.songList), 96, "amount of songs doesnt match")
        self.assertTrue(str(type(self.artist.songList[0])), "<class 'models.Song'>")

if __name__ == "__main__":
    unittest.main()
