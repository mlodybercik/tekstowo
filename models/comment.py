from datetime import datetime


class Comment:
    """Comment class.
    Local variables:
    - username (str)
    - content (str)
    - id (int)
    - timedate (timedate)
    - upVotes (int)
    - url (str)
    - childComments (list of Comment)

    Local methods:
     - None

    Static variables:
     - month - Containing all twelve months lmao
    """

    month = {"stycznia": 1,
             "lutego": 2,
             "marca": 3,
             "kwietnia": 4,
             "maja": 5,
             "czerwca": 6,
             "lipca": 7,
             "sierpnia": 8,
             "września": 9,
             "października": 10,
             "listopada": 11,
             "grudnia": 12}

    def __init__(self, username, content, id, timedate, upVotes, url, childComments=None):
        self.username = username
        self.timedate = self.__parseTimedate(timedate)
        self.content = content
        self.upVotes = upVotes
        self.url = url
        self.childComments = childComments

    def __parseTimedate(self, tab):
        # hour, minute = tab[3].split(":")
        # return datetime(int(tab[2]), self.month[tab[1]], int(tab[0]), int(hour), int(minute))
        return None
