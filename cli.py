import argparse
from itertools import islice

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--max-entries", type=int, help="print N entries", default=5)
group = parser.add_mutually_exclusive_group()
group.add_argument("-fs", "--find-song", action="store_true", help="find song by its name")
group.add_argument("-fa", "--find-artist", action="store_true", help="find artist by its name")

parser.add_argument("name", help="name of artist or song")
args = parser.parse_args()

if args.max_entries > 30 or args.max_entries < 0:
    args.max_entries = 5

from tekstowo import searchSong, searchArtist
if args.find_artist:
    query = searchArtist(args.name)
elif args.find_song:
    query = searchSong(args.name)
else:
    exit(-1)

for index, entry in islice(enumerate(query), None, args.max_entries, None):
    print(f"{index+1}.\t{entry.name}")
try:
    en = int(input("Show #"))
except ValueError:
    print("Wrong number")
    exit(-1)
if not (en > args.max_entries or en < 0):
    if args.find_artist:
        artist = query[en-1].getArtistObject()
        print(f"Name: {artist.name}")
        print(f"About: {artist.aboutArtist}")
        print(f"# of songs: {len(artist.songList)}")
    else:
        song = query[en-1].getLyricsObject()
        if song.hasText:
            print(f"{song.text}")
    exit(0)
