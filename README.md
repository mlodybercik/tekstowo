### Dev branch
Currently working on rewriting whole tekstowo to be more *classy*

## About 75% done
I've created whole thing with python classes in mind. Everything I am doing here
is just for my self-development. I created whole thing to scrap fast lots of
old song lyrics for my other private Char-RNN learning project.

*Maybe it will be useful for someone?*

## What is done?

- Everything is now a class
```python
class Lyrics:
class Artist:
class Song:
class Comment:
class ArtistSearch(Search):
class SongSearch(Search):
```
There is way of easy interaction inside tekstowo.py.

## Usage?

```python
tekstowo = Tekstowo()
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
