import logging
import re
from collections import defaultdict
from urllib.parse import urljoin

import requests_cache
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (
     BASE_DIR, CONSOLE_ARGS, DOWNLOADS_DIR,
     DOWNLOAD_SUCCESSFUL, EXPECTED_STATUS, FINISH_MESSAGE,
     MAIN_DOC_URL, PEP_URL, START_MESSAGE
)
from exceptions import ParserFindTagException
from outputs import control_output
from utils import find_tag, get_soup


def whats_new(session):
    """Парсер информации из статей о нововведениях в Python."""
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    soup = get_soup(session, whats_new_url)

    sections_by_python = soup.select(
        '#what-s-new-in-python div.toctree-wrapper li.toctree-l1'
    )

    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    for section in tqdm(sections_by_python):
        version_a_tag = section.find('a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)
        try:
            soup = get_soup(session, version_link)

            h1 = find_tag(soup, 'h1')
            dl = find_tag(soup, 'dl')
            dl_text = dl.text.replace('\n', ' ')
            results.append((version_link, h1.text, dl_text))
        except ConnectionError as error:
            logging.info(f'Отсутствует соединение с сайтом {error}')
            continue
    return results


def latest_versions(session):
    """Парсер статусов версий Python."""
    soup = get_soup(session, MAIN_DOC_URL)

    sidebar = find_tag(soup, 'div', attrs={'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')

    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise ParserFindTagException('Ничего не нашлось')

    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append((a_tag['href'], version, status))

    return results


def download(session):
    """Парсер, который скачивает архив документации Python."""
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    soup = get_soup(session, downloads_url)

    main_tag = find_tag(soup, 'div', {'role': 'main'})
    table_tag = find_tag(main_tag, 'table', {'class': 'docutils'})
    pdf_a4_tag = find_tag(table_tag, 'a',
                          {'href': re.compile(r'.+pdf-a4\.zip$')})
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]

    DOWNLOADS_DIR = BASE_DIR / 'downloads'
    DOWNLOADS_DIR.mkdir(exist_ok=True)
    archive_path = DOWNLOADS_DIR / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(DOWNLOAD_SUCCESSFUL.format(archive_path=archive_path))


def pep(session):
    """Парсинг документов PEP."""
    soup = get_soup(session, PEP_URL)
    section_tag = find_tag(soup, 'section', attrs={'id': 'numerical-index'})
    tbody_tag = find_tag(section_tag, 'tbody')
    tr_tags = tbody_tag.find_all('tr')

    error_messages = []
    results = defaultdict(int)

    for tr_tag in tqdm(tr_tags):
        data = list(find_tag(tr_tag, 'abbr').text)
        preview_status = data[1:][0] if len(data) > 1 else ''
        url = urljoin(PEP_URL, find_tag(tr_tag, 'a', attrs={
            'class': 'pep reference internal'})['href'])
        soup = get_soup(session, url)
        table_info = find_tag(soup, 'dl',
                              attrs={'class': 'rfc2822 field-list simple'})
        status_pep_page = table_info.find(
            string='Status').parent.find_next_sibling('dd').string
        if status_pep_page not in EXPECTED_STATUS[preview_status]:
            error_messages.append(f'Несовпадающие статусы:\n'
                             f'{url}\n'
                             f'Статус в карточке: {status_pep_page}\n'
                             f'Ожидаемые статусы: '
                             f'{EXPECTED_STATUS[preview_status]}')
        results[status_pep_page] += 1

    for error_message in error_messages:
        logging.warning(error_message)

    return  [
        ('Статус', 'Количество'),
        results.items(),
        ('Всего', sum(results.values())),
    ] 


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    configure_logging()
    logging.info(START_MESSAGE)
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(CONSOLE_ARGS.format(args=args))
    try:
        session = requests_cache.CachedSession()
        if args.clear_cache:
            session.cache.clear()
        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)

        if results is not None:
            control_output(results, args)
    except Exception as error:
        logging.exception(f'Ошибка при выполнении {error}', stack_info=True)
    logging.info(FINISH_MESSAGE)


if __name__ == '__main__':
    main()
