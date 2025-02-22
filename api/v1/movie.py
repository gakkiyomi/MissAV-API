import logging
from typing import Annotated

import requests
from fastapi import APIRouter, Query, Request
from lxml import html

from api.common.constants import HEADERS
from api.common.pasrer import (
    parse_login,
    parse_movie_detail,
    parse_movie_list,
    parse_movie_search,
    parse_uncensored_moives,
    parse_url,
)
from api.common.util import movie_get, param_handler
from api.domain.auth import AuthKeyDepend
from api.domain.model import BaseResponse, PageResult

logger = logging.getLogger(__name__)
app = APIRouter(
    prefix='/movie',
)


@app.get("/number/{number}",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="Get movie by specified number",
         description="Get movie by specified number")
async def get_movie(request: Request, cookies: AuthKeyDepend, number: str):
    response = requests.get(
        url=parse_url(
            f'https://missav.ai/{request.state.lang}/{number}'),
        cookies=cookies,
        headers=HEADERS, verify=False)
    if response.status_code == 200:
        logger.info(response.text)
        tree = html.fromstring(response.text)
        parse_login(tree)
        ret = parse_movie_detail(tree)
        return BaseResponse(data=ret)


@app.get("/search/{keyword}",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="search moive from missav",
         description="search moive from missav")
async def search(request: Request, cookies: AuthKeyDepend,
                 keyword: str,
                 page: int = 1,
                 filters: Annotated[str | None, Query(...,
                                                      title="moive filter query",
                                                      description="individual | jav | asiaav | uncensored-leak | uncensored | chinese-subtitle | english-subtitle")] = None,
                 sort: Annotated[str | None, Query(...,
                                                   title="sort param",
                                                   description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):
    response = requests.get(
        url=parse_url(
            f'https://missav.ai/{request.state.lang}/search/{keyword}'),
        cookies=cookies,
        params=param_handler(request.query_params),
        headers=HEADERS, verify=False)
    if response.status_code == 200:
        logger.info(response.text)
        tree = html.fromstring(response.text)
        parse_login(tree)
        ret = parse_movie_search(tree)
        return BaseResponse(data=PageResult(current_page=request.query_params.get('page'), page_size=ret[0], page_count=ret[1], data=ret[2]))


@app.get("/new",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="Get the new movies",
         description="Get the new movies")
async def get_new(request: Request, cookies: AuthKeyDepend,
                  page: int = 1,
                  filters: Annotated[str | None, Query(...,
                                                       title="moive filter query",
                                                       description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                  sort: Annotated[str | None, Query(...,
                                                    title="sort param",
                                                    description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):
    return movie_get(request=request, cookies=cookies, url=parse_url(
        f'https://missav.ai/{request.state.lang}/new'))


@app.get("/release",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="Get the latest released movies",
         description="Get the latest released movies")
async def get_release(request: Request, cookies: AuthKeyDepend,
                      page: int = 1,
                      filters: Annotated[str | None, Query(...,
                                                           title="moive filter query",
                                                           description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                      sort: Annotated[str | None, Query(...,
                                                        title="sort param",
                                                        description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):
    return movie_get(request=request, cookies=cookies, url=parse_url(
        f'https://missav.ai/{request.state.lang}/release'))


@app.get("/hot/today",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="Get today's popular movies",
         description="Get today's popular movies")
async def get_hot_today(request: Request, cookies: AuthKeyDepend,
                        page: int = 1,
                        filters: Annotated[str | None, Query(...,
                                                             title="moive filter query",
                                                             description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                        sort: Annotated[str | None, Query(...,
                                                          title="sort param",
                                                          description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):
    return movie_get(request=request, cookies=cookies, url=parse_url(
        f'https://missav.ai/dm291/{request.state.lang}/today-hot'))


@app.get("/hot/today",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="Get today's popular movies",
         description="Get today's popular movies")
async def get_hot_today(request: Request, cookies: AuthKeyDepend,
                        page: int = 1,
                        filters: Annotated[str | None, Query(...,
                                                             title="moive filter query",
                                                             description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                        sort: Annotated[str | None, Query(...,
                                                          title="sort param",
                                                          description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):
    return movie_get(request=request, cookies=cookies, url=parse_url(
        f'https://missav.ai/dm291/{request.state.lang}/today-hot'))


@app.get("/hot/weekly",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="Get weekly's popular movies",
         description="Get weekly's popular movies")
async def get_hot_weekly(request: Request, cookies: AuthKeyDepend,
                         page: int = 1,
                         filters: Annotated[str | None, Query(...,
                                                              title="moive filter query",
                                                              description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                         sort: Annotated[str | None, Query(...,
                                                           title="sort param",
                                                           description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):
    return movie_get(request=request, cookies=cookies, url=parse_url(
        f'https://missav.ai/dm169/{request.state.lang}/weekly-hot'))


@app.get("/hot/monthly",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="Get monthly's popular movies",
         description="Get monthly's popular movies")
async def get_hot_monthly(request: Request, cookies: AuthKeyDepend,
                          page: int = 1,
                          filters: Annotated[str | None, Query(...,
                                                               title="moive filter query",
                                                               description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                          sort: Annotated[str | None, Query(...,
                                                            title="sort param",
                                                            description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):
    return movie_get(request=request, cookies=cookies, url=parse_url(
        f'https://missav.ai/dm256/{request.state.lang}/monthly-hot'))


@app.get("/vr",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="Get vr movies",
         description="Get vr movies")
async def get_vr(request: Request, cookies: AuthKeyDepend,
                 page: int = 1,
                 filters: Annotated[str | None, Query(...,
                                                      title="moive filter query",
                                                      description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                 sort: Annotated[str | None, Query(...,
                                                   title="sort param",
                                                   description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):
    return movie_get(request=request, cookies=cookies, url=parse_url(
        f'https://missav.ai/dm2091/{request.state.lang}/genres/VR'))


@app.get("/saved",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="user saved moives",
         description="user saved moives")
async def saved(request: Request, cookies: AuthKeyDepend, page: int = 1):
    response = requests.get(
        url=parse_url(f'https://missav.ai/{request.state.lang}/saved?page={page}'), cookies=cookies,
        headers=HEADERS, verify=False)
    if response.status_code == 200:
        logger.info(response.text)
        tree = html.fromstring(response.text)
        parse_login(tree)
        ret = parse_movie_list(tree)
        return BaseResponse(data=PageResult(current_page=page, page_size=ret[0], page_count=ret[1], data=ret[2]))


@app.get("/uncensored",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="get the uncensored-leak moives",
         description="get the uncensored-leak moives")
async def get_uncensored_leak(request: Request, cookies: AuthKeyDepend,
                              page: int = 1,
                              filters: Annotated[str | None, Query(...,
                                                                   title="moive filter query",
                                                                   description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                              sort: Annotated[str | None, Query(...,
                                                                title="sort param",
                                                                description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):
    response = requests.get(
        url=parse_url(
            f'https://missav.ai/dm620/{request.state.lang}/uncensored-leak'),
        cookies=cookies,
        params=param_handler(request.query_params),
        headers=HEADERS, verify=False)
    if response.status_code == 200:
        logger.info(response.text)
        tree = html.fromstring(response.text)
        parse_login(tree)
        ret = parse_uncensored_moives(tree)
        return BaseResponse(data=PageResult(current_page=page, page_size=ret[0], page_count=ret[1], data=ret[2]))


@app.get("/uncensored/fc2",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="get the uncensored fc2 moives",
         description="get the uncensored fc2 moives")
async def get_uncensored_fc2(request: Request, cookies: AuthKeyDepend,
                             page: int = 1,
                             filters: Annotated[str | None, Query(...,
                                                                  title="moive filter query",
                                                                  description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                             sort: Annotated[str | None, Query(...,
                                                               title="sort param",
                                                               description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):
    return movie_get(request=request, cookies=cookies, url=parse_url(
        f'https://missav.ai/dm97/{request.state.lang}/fc2'))


@app.get("/uncensored/tokyohot",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="get the uncensored tokyohot moives",
         description="get the uncensored tokyohot moives")
async def get_uncensored_tokyohot(request: Request, cookies: AuthKeyDepend,
                                  page: int = 1,
                                  filters: Annotated[str | None, Query(...,
                                                                       title="moive filter query",
                                                                       description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                                  sort: Annotated[str | None, Query(...,
                                                                    title="sort param",
                                                                    description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):
    return movie_get(request=request, cookies=cookies, url=parse_url(
        f'https://missav.ai/dm29/{request.state.lang}/tokyohot'))


@app.get("/uncensored/1pondo",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="get the uncensored 1pondo moives",
         description="get the uncensored 1pondo moives")
async def get_uncensored_1pondo(request: Request, cookies: AuthKeyDepend,
                                page: int = 1,
                                filters: Annotated[str | None, Query(...,
                                                                     title="moive filter query",
                                                                     description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                                sort: Annotated[str | None, Query(...,
                                                                  title="sort param",
                                                                  description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):
    return movie_get(request=request, cookies=cookies, url=parse_url(
        f'https://missav.ai/dm408463/{request.state.lang}/1pondo'))


@app.get("/uncensored/marriedslash",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="get the uncensored marriedslash moives",
         description="get the uncensored marriedslash moives")
async def get_uncensored_marriedslash(request: Request, cookies: AuthKeyDepend,
                                      page: int = 1,
                                      filters: Annotated[str | None, Query(...,
                                                                           title="moive filter query",
                                                                           description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                                      sort: Annotated[str | None, Query(...,
                                                                        title="sort param",
                                                                        description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):
    return movie_get(request=request, cookies=cookies, url=parse_url(
        f'https://missav.ai/dm24/{request.state.lang}/marriedslash'))


@app.get("/uncensored/heyzo",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="get the uncensored heyzo moives",
         description="get the uncensored heyzo moives")
async def get_uncensored_heyzo(request: Request, cookies: AuthKeyDepend,
                               page: int = 1,
                               filters: Annotated[str | None, Query(...,
                                                                    title="moive filter query",
                                                                    description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                               sort: Annotated[str | None, Query(...,
                                                                 title="sort param",
                                                                 description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):
    return movie_get(request=request, cookies=cookies, url=parse_url(
        f'https://missav.ai/dm53663/{request.state.lang}/heyzo'))


@app.get("/uncensored/xxxav",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="get the uncensored xxxav moives",
         description="get the uncensored xxxav moives")
async def get_uncensored_xxxav(request: Request, cookies: AuthKeyDepend,
                               page: int = 1,
                               filters: Annotated[str | None, Query(...,
                                                                    title="moive filter query",
                                                                    description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                               sort: Annotated[str | None, Query(...,
                                                                 title="sort param",
                                                                 description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):
    return movie_get(request=request, cookies=cookies, url=parse_url(
        f'https://missav.ai/dm29/{request.state.lang}/xxxav'))


@app.get("/uncensored/naughty4610",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="get the uncensored naughty4610 moives",
         description="get the uncensored naughty4610 moives")
async def get_uncensored_naughty4610(request: Request, cookies: AuthKeyDepend,
                                     page: int = 1,
                                     filters: Annotated[str | None, Query(...,
                                                                          title="moive filter query",
                                                                          description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                                     sort: Annotated[str | None, Query(...,
                                                                       title="sort param",
                                                                       description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):
    return movie_get(request=request, cookies=cookies, url=parse_url(
        f'https://missav.ai/dm19/{request.state.lang}/naughty4610'))


@app.get("/uncensored/naughty0930",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="get the uncensored naughty0930 moives",
         description="get the uncensored naughty0930 moives")
async def get_uncensored_naughty0930(request: Request, cookies: AuthKeyDepend,
                                     page: int = 1,
                                     filters: Annotated[str | None, Query(...,
                                                                          title="moive filter query",
                                                                          description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                                     sort: Annotated[str | None, Query(...,
                                                                       title="sort param",
                                                                       description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):
    return movie_get(request=request, cookies=cookies, url=parse_url(
        f'https://missav.ai/dm22/{request.state.lang}/naughty0930'))


@app.get("/uncensored/caribbeancom",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="get the uncensored caribbeancom moives",
         description="get the uncensored caribbeancom moives")
async def get_uncensored_caribbeancom(request: Request, cookies: AuthKeyDepend,
                                      page: int = 1,
                                      filters: Annotated[str | None, Query(...,
                                                                           title="moive filter query",
                                                                           description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                                      sort: Annotated[str | None, Query(...,
                                                                        title="sort param",
                                                                        description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):
    return movie_get(request=request, cookies=cookies, url=parse_url(
        f'https://missav.ai/dm584255/{request.state.lang}/caribbeancom'))


@app.get("/uncensored/caribbeancompr",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="get the uncensored caribbeancompr moives",
         description="get the uncensored caribbeancompr moives")
async def get_uncensored_caribbeancompr(request: Request, cookies: AuthKeyDepend,
                                        page: int = 1,
                                        filters: Annotated[str | None, Query(...,
                                                                             title="moive filter query",
                                                                             description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                                        sort: Annotated[str | None, Query(...,
                                                                          title="sort param",
                                                                          description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):
    return movie_get(request=request, cookies=cookies, url=parse_url(
        f'https://missav.ai/dm8246/{request.state.lang}/caribbeancompr'))


@app.get("/uncensored/10musume",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="get the uncensored 10musume moives",
         description="get the uncensored 10musume moives")
async def get_uncensored_10musume(request: Request, cookies: AuthKeyDepend,
                                  page: int = 1,
                                  filters: Annotated[str | None, Query(...,
                                                                       title="moive filter query",
                                                                       description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                                  sort: Annotated[str | None, Query(...,
                                                                    title="sort param",
                                                                    description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):
    return movie_get(request=request, cookies=cookies, url=parse_url(
        f'https://missav.ai/dm620677/{request.state.lang}/10musume'))


@app.get("/uncensored/pacopacomama",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="get the uncensored pacopacomama moives",
         description="get the uncensored pacopacomama moives")
async def get_uncensored_caribbeancom(request: Request, cookies: AuthKeyDepend,
                                      page: int = 1,
                                      filters: Annotated[str | None, Query(...,
                                                                           title="moive filter query",
                                                                           description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                                      sort: Annotated[str | None, Query(...,
                                                                        title="sort param",
                                                                        description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):
    return movie_get(request=request, cookies=cookies, url=parse_url(
        f'https://missav.ai/dm12454/{request.state.lang}/pacopacomama'))


@app.get("/uncensored/gachinco",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="get the uncensored gachinco moives",
         description="get the uncensored gachinco moives")
async def get_uncensored_caribbeancom(request: Request, cookies: AuthKeyDepend,
                                      page: int = 1,
                                      filters: Annotated[str | None, Query(...,
                                                                           title="moive filter query",
                                                                           description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                                      sort: Annotated[str | None, Query(...,
                                                                        title="sort param",
                                                                        description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):
    return movie_get(request=request, cookies=cookies, url=parse_url(
        f'https://missav.ai/dm135/{request.state.lang}/gachinco'))


@app.get("/asia-av/madou",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="get the madou moives",
         description="get the madou moives")
async def get_madou(request: Request, cookies: AuthKeyDepend,
                    page: int = 1,
                    filters: Annotated[str | None, Query(...,
                                                         title="moive filter query",
                                                         description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                    sort: Annotated[str | None, Query(...,
                                                      title="sort param",
                                                      description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):
    return movie_get(request=request, cookies=cookies, url=parse_url(
        f'https://missav.ai/dm34/{request.state.lang}/madou'))


@app.get("/asia-av/twav",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="get the twav moives",
         description="get the twav moives")
async def get_twav(request: Request, cookies: AuthKeyDepend,
                   page: int = 1,
                   filters: Annotated[str | None, Query(...,
                                                        title="moive filter query",
                                                        description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                   sort: Annotated[str | None, Query(...,
                                                     title="sort param",
                                                     description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):
    return movie_get(request=request, cookies=cookies, url=parse_url(
        f'https://missav.ai/dm17/{request.state.lang}/twav'))


@app.get("/asia-av/furuke",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="get the furuke moives",
         description="get the furuke moives")
async def get_furuke(request: Request, cookies: AuthKeyDepend,
                     page: int = 1,
                     filters: Annotated[str | None, Query(...,
                                                          title="moive filter query",
                                                          description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                     sort: Annotated[str | None, Query(...,
                                                       title="sort param",
                                                       description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):
    return movie_get(request=request, cookies=cookies, url=parse_url(
        f'https://missav.ai/dm15/{request.state.lang}/furuke'))


@app.get("/streamer/kr",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="get the klive",
         description="get the klive")
async def get_kr_streamer(request: Request, cookies: AuthKeyDepend,
                          page: int = 1,
                          filters: Annotated[str | None, Query(...,
                                                               title="moive filter query",
                                                               description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                          sort: Annotated[str | None, Query(...,
                                                            title="sort param",
                                                            description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):
    return movie_get(request=request, cookies=cookies, url=parse_url(
        f'https://missav.ai/{request.state.lang}/klive'))


@app.get("/streamer/cn",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="get the clive",
         description="get the clive")
async def get_kr_streamer(request: Request, cookies: AuthKeyDepend,
                          page: int = 1,
                          filters: Annotated[str | None, Query(...,
                                                               title="moive filter query",
                                                               description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                          sort: Annotated[str | None, Query(...,
                                                            title="sort param",
                                                            description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):
    return movie_get(request=request, cookies=cookies, url=parse_url(
        f'https://missav.ai/{request.state.lang}/clive'))


@app.get("/amateur/siro",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="get siro moives",
         description="get siro moives")
async def get_amateur_siro(request: Request, cookies: AuthKeyDepend,
                           page: int = 1,
                           filters: Annotated[str | None, Query(...,
                                                                title="moive filter query",
                                                                description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                           sort: Annotated[str | None, Query(...,
                                                             title="sort param",
                                                             description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):
    return movie_get(request=request, cookies=cookies, url=parse_url(
        f'https://missav.ai/dm23/{request.state.lang}/siro'))


@app.get("/amateur/luxu",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="get luxu moives",
         description="get luxu moives")
async def get_amateur_luxu(request: Request, cookies: AuthKeyDepend,
                           page: int = 1,
                           filters: Annotated[str | None, Query(...,
                                                                title="moive filter query",
                                                                description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                           sort: Annotated[str | None, Query(...,
                                                             title="sort param",
                                                             description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):
    return movie_get(request=request, cookies=cookies, url=parse_url(
        f'https://missav.ai/dm20/{request.state.lang}/luxu'))


@app.get("/amateur/gana",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="get gana moives",
         description="get gana moives")
async def get_amateur_gana(request: Request, cookies: AuthKeyDepend,
                           page: int = 1,
                           filters: Annotated[str | None, Query(...,
                                                                title="moive filter query",
                                                                description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                           sort: Annotated[str | None, Query(...,
                                                             title="sort param",
                                                             description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):
    return movie_get(request=request, cookies=cookies, url=parse_url(
        f'https://missav.ai/dm17/{request.state.lang}/gana'))


@app.get("/amateur/maan",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="get maan moives",
         description="get simaanro moives")
async def get_amateur_maan(request: Request, cookies: AuthKeyDepend,
                           page: int = 1,
                           filters: Annotated[str | None, Query(...,
                                                                title="moive filter query",
                                                                description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                           sort: Annotated[str | None, Query(...,
                                                             title="sort param",
                                                             description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):
    return movie_get(request=request, cookies=cookies, url=parse_url(
        f'https://missav.ai/dm862/{request.state.lang}/maan'))


@app.get("/amateur/scute",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="get scute moives",
         description="get scute moives")
async def get_amateur_scute(request: Request, cookies: AuthKeyDepend,
                            page: int = 1,
                            filters: Annotated[str | None, Query(...,
                                                                 title="moive filter query",
                                                                 description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                            sort: Annotated[str | None, Query(...,
                                                              title="sort param",
                                                              description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):
    return movie_get(request=request, cookies=cookies, url=parse_url(
        f'https://missav.ai/dm23/{request.state.lang}/scute'))


@app.get("/amateur/ara",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="get ara moives",
         description="get ara moives")
async def get_amateur_ara(request: Request, cookies: AuthKeyDepend,
                          page: int = 1,
                          filters: Annotated[str | None, Query(...,
                                                               title="moive filter query",
                                                               description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                          sort: Annotated[str | None, Query(...,
                                                            title="sort param",
                                                            description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):
    return movie_get(request=request, cookies=cookies, url=parse_url(
        f'https://missav.ai/dm19/{request.state.lang}/ara'))


@app.get("/chinese-subtitle",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="get chinese subtitle moives",
         description="get all chinese subtitle moives")
async def get_chinese_subtitle(request: Request, cookies: AuthKeyDepend,
                               page: int = 1,
                               filters: Annotated[str | None, Query(...,
                                                                    title="moive filter query",
                                                                    description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                               sort: Annotated[str | None, Query(...,
                                                                 title="sort param",
                                                                 description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):
    response = requests.get(
        url=parse_url(
            f'https://missav.ai/dm265/{request.state.lang}/chinese-subtitle'),
        cookies=cookies,
        params=param_handler(request.query_params),
        headers=HEADERS, verify=False)
    if response.status_code == 200:
        logger.info(response.text)
        tree = html.fromstring(response.text)
        parse_login(tree)
        ret = parse_movie_list(tree)
        return BaseResponse(data=PageResult(current_page=page, page_size=ret[0], page_count=ret[1], data=ret[2]))


@app.get("/english-subtitle",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="get english subtitle moives",
         description="get all english subtitle moives")
async def get_english_subtitle(request: Request, cookies: AuthKeyDepend,
                               page: int = 1,
                               filters: Annotated[str | None, Query(...,
                                                                    title="moive filter query",
                                                                    description="individual | multiple | chinese-subtitle | english-subtitle")] = None,
                               sort: Annotated[str | None, Query(...,
                                                                 title="the actress's cup",
                                                                 description="saved | released_at | published_at | today_views | weekly_views | monthly_views | views")] = None):
    response = requests.get(
        url=parse_url(
            f'https://missav.ai/dm265/{request.state.lang}/english-subtitle'),
        params=param_handler(request.query_params),
        cookies=cookies,
        headers=HEADERS, verify=False)
    if response.status_code == 200:
        logger.info(response.text)
        tree = html.fromstring(response.text)
        parse_login(tree)
        ret = parse_movie_list(tree)
        return BaseResponse(data=PageResult(current_page=page, page_size=ret[0], page_count=ret[1], data=ret[2]))


@app.get("/watch-history",
         response_model=BaseResponse,
         tags=["Movie API"],
         summary="user watch history",
         description="user watch history")
async def history(request: Request, cookies: AuthKeyDepend, page: int = 1):
    response = requests.get(
        url=parse_url(f'https://missav.ai/{request.state.lang}/history'), headers=HEADERS,
        cookies=cookies, verify=False)
    if response.status_code == 200:
        tree = html.fromstring(response.text)
        parse_login(tree)
        ret = parse_movie_list(tree)
        return BaseResponse(data=PageResult(current_page=page, page_size=ret[0], page_count=ret[1], data=ret[2]))
