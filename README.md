## About 85%(?) done

imma rewrite this readme.md

![logo](misc/py.png)

I've created whole thing with python classes in mind. Everything I am doing here
is just for my self-development. I created whole thing to scrap *fast* lots of
old song lyrics for my other private Char-RNN learning project.

*Maybe it will be useful for someone?*

## What is done?

Everything is now a class
```python
class Lyrics
class Artist
class Song
class Comment
class ArtistSearch(Search)
class SongSearch(Search)
class User
```
There is way of easy and recommendedway of interaction inside tekstowo.py.

## Usage?

```python
import tekstowo
zeppelin = tekstowo.getText("http://www.tekstowo.pl/piosenka,led_zeppelin,stairway_to_heaven.html")
if(zeppelin.hasText):
  print(zeppelin.text)
```

Function definitions are rather self-explanatory, in case of trouble use python's help() command.

### To do:
Long-term TODO
- CLI way of doing things
- Fix some of that *spaghetti*
- PyPI???
- Add classes for:
```python
class Account
class Ranking
```
Short-term TODO
- Go check "my big grand big big list of things to do" to see more things I've been working on.
