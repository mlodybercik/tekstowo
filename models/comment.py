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
    - replyID (int)

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

    def __init__(self, username, content, id, timedate, upVotes, url, replyID=None, childComments=None):
        self.username = username
        self.content = content
        self.upVotes = int(upVotes)
        self.url = url
        self.timedate = self.__parseTimedate(timedate)
        self.childComments = childComments

        if childComments is None:
            self.childComments = []
        else:
            self.childComments = childComments

        if replyID is None:
            self.replyID = 0
        else:
            self.replyID = int(replyID)

        if id is None:
            self.id = 0
        else:
            self.id = int(id)

    def __parseTimedate(self, tab):
        if tab == 0:
            return None
        else:
            hour, minute = tab[3].split(":")
            return datetime(int(tab[2]), self.month[tab[1]], int(tab[0]), int(hour), int(minute))
