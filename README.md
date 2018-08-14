# tekstowoLyrics

Web scraper for an (ancient) polish website with lyrics and stuff.
[tekstowo.pl](http://www.tekstowo.pl/)

## usage

It's easy!

### terminal

```shell
python tekstowo.py -h                                            

usage: tekstowo.py [-h] (-g | -a | -s type | -i | -x) name_url [amount]

CLI tekstowo wrapper.

positional arguments:
  name_url    of an artist or song
  amount      of displayed results

optional arguments:
  -h, --help  show this help message and exit
  -g          get song lyrics [URL]
  -a          returns all songs of an artist [name]
  -s type     search for an n amount of things
  -i          get info from the website [URL]
  -x          returns all songs lyrics in one go [name]
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
#You can supply tekstowo class with requests headers.
tekstowo = Tekstowo(headers={'user-agent': 'rick_astley/0.0.1'})
tekstowo.getText("/piosenka,rick_astley,never_gonna_give_you_up.html")
...
```
