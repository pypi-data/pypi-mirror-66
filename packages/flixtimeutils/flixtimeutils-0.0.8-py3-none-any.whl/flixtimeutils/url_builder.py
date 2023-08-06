from enum import Enum

from flixtimeutils.user_agent import UserAgent


class DataSource(Enum):
    THE_MOVIE_DATABASE = 1
    UNOGS = 2


class UrlBuilder:

    def __init__(self, data_source: DataSource, user_agent: UserAgent, environment: dict):
        """
        Parameters
        ----------
        data_source : DataSource
            The data source to build urls for
        user_agent : DataSource
            The user agent passed in the request

        """
        self.data_source = data_source
        self.user_agent = user_agent
        self.environment = environment

    def build_url(self, path: str, parameters: dict = {}) -> str:
        """
        This method will build the url based on the passed arguments.

        Parameters
        ----------
        path : str
            The path of the url that will be build
        parameters : dict
            The query parameters of the url.

        Returns
        -------
        The url string build with the passed arguments.

        Raises
        ------
        ValueError

        """
        base_url = self._base_url()
        all_parameters = parameters.copy()
        all_parameters.update(self._default_parameters())

        query_items = '&'.join(['='.join((key, str(value))) for key, value in all_parameters.items()])

        format_url = '{base_url}{path}?{query_items}'
        return format_url.format(base_url=base_url, path=path, query_items=query_items)

    def build_headers(self) -> dict:
        if self.data_source == DataSource.THE_MOVIE_DATABASE:
            return {}
        elif self.data_source == DataSource.UNOGS:
            return {
                'x-rapidapi-host': self.environment["UNOGSAPIHOST"],
                "x-rapidapi-key": self.environment["UNOGSAPIKEY"]
            }
        else:
            raise ValueError

    def _base_url(self) -> str:
        if self.data_source == DataSource.THE_MOVIE_DATABASE:
            return 'https://api.themoviedb.org'
        elif self.data_source == DataSource.UNOGS:
            return 'https://unogsng.p.rapidapi.com'
        else:
            raise ValueError

    def _default_parameters(self) -> dict:
        if self.data_source == DataSource.THE_MOVIE_DATABASE:
            return {
                'api_key': self.environment["TMDBAPIKEY"],
                'language': self.user_agent.language
            }
        elif self.data_source == DataSource.UNOGS:
            return {}
        else:
            raise ValueError
