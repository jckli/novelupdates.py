from .request import Request
from .parseFeed import parseFeed


class Client:
    def __init__(self):
        """
        Initialize the client.
        """
        self.req = Request()
        
    def getLatestFeed(self):
        req = self.req.get("https://www.novelupdates.com/")
        return parseFeed(req)