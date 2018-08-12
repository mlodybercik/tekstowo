# tekstowoLyrics

Web scraper for an (ancient) polish website with lyrics and stuff.
[tekstowo.pl](http://www.tekstowo.pl/)

## usage

It's easy!

### terminal

```shell
python tekstowo.py -h
usage: tekstowo.py [-h]
                   (--getText /URL.html | --searchArtist name n --searchSong artist n | --getSongs song name | --giveMeAll artist)

CLI tekstowo wrapper.

optional arguments:
  -h, --help            show this help message and exit
  --getText /URL.html, -g /URL.html
                        get song lyrics
  --searchArtist name n name n, -s name n name n
                        search for an n amount of artists
  --searchSong artist n artist n, -S artist n artist n
                        search for n amount of songs
  --getSongs song name, -a song name
                        returns all songs of an artist
  --giveMeAll artist, -x artist
                        returns all songs lyrics in one go
```                  

```shell
python tekstowo.py -S "never gonna give you up" 3
Rick Astley - Never gonna give you up: /piosenka,rick_astley,never_gonna_give_you_up.html
Ashley Tisdale - Never Gonna Give you up: /piosenka,ashley_tisdale,never_gonna_give_you_up.html
BBMak - Never gonna give you up: /piosenka,bbmak,never_gonna_give_you_up.html
```

### python

```python
from tekstowo import Tekstowo
#You can also supply tekstowo class with requests headers.
tekstowo = Tekstowo(headers={'user-agent': 'rick_astley/0.0.1'})
tekstowo.getText("/piosenka,rick_astley,never_gonna_give_you_up.html")
...
```
