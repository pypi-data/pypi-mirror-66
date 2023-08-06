import logging
from typing import Callable, Dict

import ssl
import urllib.request
import urllib.error
import time

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

__all__ = ['get_soup', 'PARSER_DICT']


def get_soup(url: str, num_of_attempts: int = 3, delay: float = 0.5) -> BeautifulSoup or None:
    if num_of_attempts == -1:
        return
    try:
        html = urllib.request.urlopen(url, context=_get_context()).read()
        logger.info(f'Successfully parsed url.')
        return BeautifulSoup(html, 'html.parser')
    except Exception as err:
        logger.exception(err)
        logger.info(f'Another try in {delay} sec. Number of attempts remained: {num_of_attempts}.')
        time.sleep(delay)
        return get_soup(url, num_of_attempts - 1)


def _get_context() -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def _parse_wg(debug: bool = False, **kwargs) -> str:
    url = 'https://www.wg-gesucht.de/wohnungen-in-Tuebingen' \
          '.127.2.1.0.html?offer_filter=1&sort_column=0&noDeact' \
          '=1&city_id=127&category=2&rent_type=0&sMin=30&rMax=1500'

    soup = get_soup(url, **kwargs)
    if debug:
        return soup
    return soup.find_all('div', {'class': 'card_body'})[1].find('h3').find('a').text.strip()


PARSER_DICT: Dict[str, Callable] = {
    'WG': _parse_wg
}
