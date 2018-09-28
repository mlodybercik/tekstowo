### Dev branch
Currently working on rewriting whole tekstowo to be more *classy*

## About 75% done
I've created whole thing with python classes in mind. Everything I am doing here
is just for my self-development. (And maybe for someone who will need to get info using my scraper? 🤔

## What is done?

- Everything is now a class
```python
class Utils:
class Lyrics:
class Artist:
class Song:
class Comment:
```
- Everything runs a little bit faster.

## Usage?

```python
tekstowo = Tekstowo()
zeppelin = tekstowo.getText("http://www.tekstowo.pl/piosenka,led_zeppelin,stairway_to_heaven.html")
if(zeppelin.hasText):
  print(zeppelin.text)
```

Function definitions are rather self-explanatory, in case of trouble use python help command.

### To do:
- Add classes for:
```python
class Account
class RankingEntry
class SearchEntry
```
- Fix **spaghetti** code
