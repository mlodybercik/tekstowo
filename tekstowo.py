"""Main file for tekstowo.py"""
import models


def login(username, password, session=models.session):
    """Log default session in to use features of logged in user."""
    session.login(username, password)


def logout(session=models.session):
    """Logout account. Alias of models.session.logout.
    Be sure to logout before killing python or it will throw Exceptions."""
    session.logout()


def getText(url, session=models.session):
    """Downloads lyrics and some other stuff from site.
    See models/* for more.
    *(whole url, starting with https://...)*"""
    return models.Lyrics.fromUrl(url, session)


def getArtist(url, session=models.session):
    """Downloads artist info and some other stuff from site.
    See models/* for more.
    *(whole url, starting with https://...)*"""
    return models.Artist.fromUrl(url, session)


def getUser(username, session=models.session):
    """Downloads information about user."""
    return models.User.fromLogin(username, session)


def searchArtist(artistName, session=models.session):
    """Search for artist. Returns models.ArtistSearch"""
    return models.ArtistSearch(artistName, session)


def searchSong(name, session=models.session):
    """Search for lyrics. Returns models.SongSearch"""
    return models.SongSearch(name, session)


def getAllTexts(artist_name=None, artist_url=None, session=models.session):
    """Generator object for getting all lyrics of given artist."""
    if artist_name:
        artist = searchArtist(artist_name, session)[0].getArtistObject()
    elif artist_url:
        artist = getArtist(artist_url, session)
    else:
        raise models.exceptions.TekstowoBadObject("No parameters passed.")
    for i in artist.songList:
        yield i.getLyricsObject().text
    return
