from bs4 import BeautifulSoup
from requests import RequestException

from exceptions import ParserFindTagException


CONNECTION_ERROR = 'Возникла ошибка {error} при загрузке страницы {url}'
TAG_NOT_FOUND = 'Не найден тег {tag} {attrs}'


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
        raise ParserFindTagException(
            TAG_NOT_FOUND.format(tag=tag, attrs=attrs)
        )
    return searched_tag


def get_soup(session, url, features='lxml'):
    return BeautifulSoup(get_response(session, url).text, features)
