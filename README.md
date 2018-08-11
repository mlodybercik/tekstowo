# tekstowoLyrics

Web scraper for an (ancient) polish website with lyrics and stuff.
[tekstowo.pl](http://www.tekstowo.pl/)

## usage

It's easy!

### terminal

```shell
python tekstowo.py -h
usage: tekstowo.py [-h]
                   (--getText URL | --searchArtist name | --getSongs name | --giveMeAll name)

CLI tekstowo wrapper.

optional arguments:
  -h, --help            show this help message and exit
  --getText URL, -g URL
                        get song lyrics
  --searchArtist name, -s name
                        search for an artist
  --getSongs name, -a name
                        returns all songs of an artist
  --giveMeAll name, -x name
                        returns all songs lyrics in one go

    python tekstowo.py -g /piosenka,rick_astley,never_gonna_give_you_up.html
    We re no strangers to love
    You know the rules and so do I
    ...
```

### python

```python
from tekstowo import Tekstowo

tekstowo = Tekstowo()
tekstowo.getText("/piosenka,rick_astley,never_gonna_give_you_up.html")
...
```
