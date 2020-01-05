import models


def login(login, password):
    models.session.login(login, password)


def getText(url, session=models.session):
    """Downloads lyrics and some other stuff from site.
    See models/* for more.
    *(whole url, starting with https://...)*"""
    return models.Lyrics.from_url(url)


def getArtist(url):
    """Downloads artist info and some other stuff from site.
    See models/* for more.
    *(whole url, starting with https://...)*"""
    return models.Artist.from_url(url)


def searchArtist(artistName):
    """Search for artist. Returns models.ArtistSearch"""
    return models.ArtistSearch(artistName)


def searchSong(name):
    """Search for lyrics. Returns models.SongSearch"""
    return models.SongSearch(name)


def getAllTexts(artist_name=None, artist_url=None):
    """Generator object for getting all lyrics of given artist."""
    if artist_name:
        artist = searchArtist(artist_name)[0].getArtistObject()
    elif artist_url:
        artist = getArtist(artist_url)
    else:
        raise StopIteration("No parameters passed.")
    for i in artist.songList:
        yield i.getLyricsObject().text
