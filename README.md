<img src="https://raw.githubusercontent.com/krzesu0/tekstowo/dev/misc/py.png" height="100px">

# tekstowo.py
**Tekstowo is a parser and a way for interaction with [Tekstowo](https://www.tekstowo.pl/) using Python with classes in mind.**

## tekstowo.pl

[Tekstowo](https://www.tekstowo.pl/) is a *big* site made for finding song lyrics, song translations to polish and soundtracks with very subtle social media approach. It has **>1 600 000** texts right now, with about *1 000* more waiting to be approved at any time. It's nowhere close to international giant like Genius.


## My tekstowo
Project begun some time ago when I was playing with CharNN's to *"create"* my own music. I quickly created something to parse site and dump all lyrics into one big file. Later I had too much free time so I spent it working more and more on this parser.


## Usage
As I said, it is created with classes in mind, so everything is represented as an object. Main file, `tekstowo.py` contains a way of interaction with models.
Most of objects are rather self explenatory. Currently implemented classes:
 - `Artist` - contains information about an Artist. duuh.
 - `Lyrics` - text, translation, id, upvotes, comments...
 - `Comment` - id, comment body, url, child comments...
 - Draft Objects - `Song`, `ArtistDraft`, `UserDraft`.
 - `Search` - used only to search for artist and song.
 - `User` - name, sex, rank, points...
 
## Examples:
```python
import tekstowo
zeppelin = tekstowo.getText("http://www.tekstowo.pl/piosenka,led_zeppelin,stairway_to_heaven.html")
if(zeppelin.hasText):
  print(zeppelin.text)
```
```python
user = tekstowo.getUser("bombelbombel") # he is no1 rn
print(user.name)
for i in user.getLyrics():
  print(i.url)
```
```python
for i in tekstowo.getAllTexts("Red Hot Chili Peppers"):
  print(i)
```
Function definitions are rather self-explanatory, in case of trouble use python's help() command.
