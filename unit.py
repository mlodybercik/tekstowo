import unittest
import models


class TestLyrics(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        x = models.Utils()
        y = x.getWebsite("http://www.tekstowo.pl/piosenka,rick_astley,never_gonna_give_you_up.html")
        self.lyrics = models.Lyrics(y)

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
        self.utils = models.Utils()
        self.artist = models.Artist(self.utils.getWebsite("http://www.tekstowo.pl/wykonawca,rick_astley.html"))

    def test_Name(self):
        self.assertEqual(self.artist.name, "Rick Astley", "name doesen't match")

    def test_Albums(self):
        self.assertTrue(len(self.artist.albums) == 9, "albums doesn't match")

    def test_AmountOfFans(self):
        self.assertGreaterEqual(self.artist.amountOfFans, 9, "fans doesn't match")

    def test_songList(self):
        self.assertEqual(len(self.artist.songList), 107, "amount of songs doesnt match")
        self.assertTrue(str(type(self.artist.songList[0])), "<class 'models.Song'>")


class TestArtistSearch(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		self.searchArtist = models.ArtistSearch("Rick Astley")
		self.artistObject = None
		self.artist = None

	def test_Find(self):
		self.assertTrue(self.searchArtist[0].url == "/piosenki_artysty,rick_astley.html")

	def test_GetArtistObject(self):
		self.artistObject = self.searchArtist[0].getArtistObject()
		self.assertTrue(type(self.artistObject) == models.Artist)

	def test_something(self):
		pass

if __name__ == "__main__":
    unittest.main()
