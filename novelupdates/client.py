from .request import Request
from . import parsers


class Client:
    def __init__(self):
        self.req = Request()
        
    def get_latest_feed(self):
        """Gets the latest updates from NovelUpdates.

        Parameters
        ----------
        None

        Returns
        -------
        :class:`list`
            A dictionary containing the latest novel updates from NovelUpdates.
            Contains all information and links for each update.
        """
        req = self.req.get("https://www.novelupdates.com/")
        return parsers.parseFeed(req)

    def search_series(self, name):
        """Searches for a series and gets back the top 25 results (first page).

        Parameters
        ----------
        name : :class:`str`
            The name of the series to search for.

        Returns
        -------
        :class:`list`
            A dictionary containing the top 25 results for the search.
            Contains all information and links for each result.
        """
        req = self.req.get(f"https://www.novelupdates.com/?s={name}")
        return parsers.parseSearch(req)

    def series_info(self, series_id):
        """Gets information about a series.

        Parameters
        ----------
        id : :class:`int`
            The id of the series. (/series/{ID})

        Returns
        -------
        :class:`dict`
            A dictionary containing information about the series.
            Contains all information and links for the series.
        """
        req = self.req.get(f"https://www.novelupdates.com/series/{series_id}")
        return parsers.parseSeries(req)