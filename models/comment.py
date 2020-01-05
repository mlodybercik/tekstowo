from datetime import datetime
from .utils import month


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

    def __str__(self):
        return "{}: {}".format(self.username, self.content)

    def __repr__(self):
        return "Comment: {}".format(self.username)

    def __int__(self):
        return self.id

    def __getitem__(self, n):
        return self.childComments

    def __parseTimedate(self, tab):
        if tab == 0:
            return None
        else:
            hour, minute = tab[3].split(":")
            return datetime(int(tab[2]), month[tab[1]], int(tab[0]), int(hour), int(minute))
