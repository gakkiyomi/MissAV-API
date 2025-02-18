import logging

import requests
from fastapi import Request
from lxml import html

from api.common.constants import HEADERS
from api.common.pasrer import parse_login, parse_movie_list
from api.domain.model import BaseResponse, PageResult

logger = logging.getLogger(__name__)


def param_handler(raw_params: dict) -> dict:
    return {k: v for k, v in raw_params.items() if v not in [
            None, ""]}


def movie_get(request: Request, cookies: dict, url: str) -> BaseResponse:
    response = requests.get(
        url=url,
        cookies=cookies,
        params=param_handler(request.query_params),
        headers=HEADERS, verify=False)
    if response.status_code == 200:
        logger.info(response.text)
        tree = html.fromstring(response.text)
        parse_login(tree)
        ret = parse_movie_list(tree)
        return BaseResponse(data=PageResult(current_page=request.query_params.get('page'), page_size=ret[0], page_count=ret[1], data=ret[2]))
