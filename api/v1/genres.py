import logging
from typing import Annotated

import requests
from fastapi import APIRouter, Query, Request
from lxml import html

from api.common.constants import HEADERS
from api.common.pasrer import parse_login, parse_movie_genres, parse_url
from api.common.util import movie_get
from api.domain.auth import AuthKeyDepend
from api.domain.model import BaseResponse, PageResult

logger = logging.getLogger(__name__)
app = APIRouter(
    prefix='/genres',
)


@app.get("",
         response_model=BaseResponse,
         tags=["Genres API"],
         summary="Get all movie's Geners",
         description="Get all movie's Geners")
async def get_genres(request: Request, cookies: AuthKeyDepend,
                     page: int = 1):
    response = requests.get(
        url=parse_url(f'https://missav.ai/{request.state.lang}/genres?page={page}'), headers=HEADERS,
        cookies=cookies, verify=False)
    if response.status_code == 200:
        tree = html.fromstring(response.text)
        parse_login(tree)
        ret = parse_movie_genres(tree)
        return BaseResponse(data=PageResult(current_page=page, page_size=ret[0], page_count=ret[1], data=ret[2]))


@app.get("/{name}",
         response_model=BaseResponse,
         tags=["Genres API"],
         summary="Query genres from specific name",
         description="Query genres from specific name")
async def get_genres_detail(request: Request, cookies: AuthKeyDepend, name: str,
                            filters: Annotated[str | None, Query(...,
                                                                 title="moive filter query",
                                                                 description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                            sort: Annotated[str | None, Query(...,
                                                              title="sort param",
                                                              description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None,
                            page: int = 1):
    url = parse_url(f'https://missav.ai/{request.state.lang}/genres/{name}')
    return movie_get(request, cookies, url)
