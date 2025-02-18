import logging
from typing import Annotated

import requests
from fastapi import APIRouter, Query, Request
from fastapi.datastructures import QueryParams
from lxml import html

from api.common.constants import HEADERS
from api.common.pasrer import (
    parse_actress_list,
    parse_actress_ranking,
    parse_login,
    parse_url,
)
from api.common.util import movie_get, param_handler
from api.domain.auth import AuthKeyDepend
from api.domain.model import BaseResponse, PageResult

logger = logging.getLogger(__name__)
app = APIRouter(
    prefix='/actress',
)


@app.get("/movies/{name}",
         response_model=BaseResponse,
         tags=["ACTRESS API"],
         summary="get actress movies ",
         description="get actress movies from specify name")
async def get_movies(request: Request, cookies: AuthKeyDepend, name: str, page: int = 1,
                     filters: Annotated[str | None, Query(...,
                                                          title="moive filter query",
                                                          description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                     sort: Annotated[str | None, Query(...,
                                                       title="sort param",
                                                       description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):

    return movie_get(request, cookies, parse_url(f'https://missav.ai/{request.state.lang}/actresses/{name}'))


@app.get("/saved",
         response_model=BaseResponse,
         tags=["ACTRESS API"],
         summary="user saved actress",
         description="user saved actress")
async def saved(request: Request, cookies: AuthKeyDepend, page: int = 1):
    response = requests.get(
        url=parse_url(f'https://missav.ai/{request.state.lang}/saved/actresses?page={page}'), cookies=cookies,
        headers=HEADERS, verify=False)
    if response.status_code == 200:
        logger.info(response.text)
        tree = html.fromstring(response.text)
        parse_login(tree)
        ret = parse_actress_list(tree)
        return BaseResponse(data=PageResult(current_page=page, page_size=ret[0], page_count=ret[1], data=ret[2]))


@app.get("/ranking",
         response_model=BaseResponse,
         tags=["ACTRESS API"],
         summary="actress ranking",
         description="actress ranking")
async def ranking(request: Request, cookies: AuthKeyDepend):
    response = requests.get(
        url=parse_url(f'https://missav.ai/{request.state.lang}/actresses/ranking'), cookies=cookies,
        headers=HEADERS, verify=False)
    if response.status_code == 200:
        logger.info(response.text)
        tree = html.fromstring(response.text)
        parse_login(tree)
        ret = parse_actress_ranking(tree)
        return BaseResponse(data=ret)


@app.get("/list",
         response_model=BaseResponse,
         tags=["ACTRESS API"],
         summary="actress list",
         description="get all actress")
async def list(request: Request, cookies: AuthKeyDepend,
               page: int = 1,
               height: Annotated[str | None, Query(...,
                                                   title="the actress's height",
                                                   description="160-175")] = None,
               cup: Annotated[str | None, Query(...,
                                                title="the actress's cup",
                                                description="A - H")] = None,
               age: Annotated[str | None, Query(...,
                                                title="the actress's age",
                                                description="25-30")] = None,
               debut: Annotated[str | None, Query(...,
                                                  title="the actress's debut time",
                                                  description="2020")] = None,
               sort: Annotated[str | None, Query(...,
                                                 title="sort param",
                                                 description="debug | videos")] = None):
    response = requests.get(
        url=parse_url(f'https://missav.ai/{request.state.lang}/actresses'), cookies=cookies,
        params=param_handler(request.query_params),
        headers=HEADERS, verify=False)
    if response.status_code == 200:
        logger.info(response.text)
        tree = html.fromstring(response.text)
        parse_login(tree)
        ret = parse_actress_list(tree)
        return BaseResponse(data=PageResult(current_page=page, page_size=ret[0], page_count=ret[1], data=ret[2]))
