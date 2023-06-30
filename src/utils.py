from bs4 import BeautifulSoup
from requests import RequestException

from constants import CONNECTION_ERROR, TAG_NOT_FOUND
from exceptions import ParserFindTagException


def get_response(session, url, encoding='utf-8'):
    """Перехват ошибки RequestException."""
    try:
        response = session.get(url)
        response.encoding = encoding
        return response
    except RequestException as error:
        raise ConnectionError(CONNECTION_ERROR.format(error=error, url=url))


def find_tag(soup, tag, attrs=None):
    """Перехват ошибки поиска тегов."""
    searched_tag = soup.find(tag, attrs=({} if attrs is None else attrs))
    if searched_tag is None:
        error_message = TAG_NOT_FOUND.format(tag=tag, attrs=attrs)
        raise ParserFindTagException(error_message)
    return searched_tag


def get_soup(session, url, features='lxml'):
    response = get_response(session, url)
    return BeautifulSoup(response.text, features)
