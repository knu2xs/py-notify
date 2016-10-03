# import modules
import bitly_api
import json


def get_short_url(long_url, login=None, api_key=None):
    """
    Get shortened url using bit.ly.
    :param long_url: Long url to be shortened.
    :param login: Bitly login for api.
    :param api_key: Bitly api key corresponding to the login.
    :return: Strung shortened url.
    """
    # if the credentials are provided
    if login and api_key:

        # get a connection using provided credentials
        connection = bitly_api.Connection(login=login, api_key=api_key)

    else:

        # open the configuration file with the credentials
        credentials_file = open('resources/credentials.json').read()
        credentials_all = json.loads(credentials_file)
        credentials = credentials_all['bitly']

        # get a secure connection using credentials
        connection = bitly_api.Connection(login=credentials['login'], api_key=credentials['api_key'])

    # shorten the url and return the result
    return connection.shorten(uri=long_url)
