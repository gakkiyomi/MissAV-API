import logging

import requests
from fastapi import APIRouter, Path, Request
from lxml import html

from api.common.constants import HEADERS
from api.common.pasrer import (
    parse_login,
    parse_playlist_delete_token,
    parse_playlist_detail,
    parse_playlists,
    parse_url,
)
from api.domain.auth import AuthKeyDepend
from api.domain.model import BaseResponse, PageResult, PlaylistInput

logger = logging.getLogger(__name__)
app = APIRouter(
    prefix='/playlists',
)


@app.get("",
         response_model=BaseResponse,
         tags=["Playlist API"],
         summary="playlists",
         description="get all playlists of user")
async def playlists(request: Request, cookies: AuthKeyDepend, page: int = 1):
    response = requests.get(
        url=parse_url(f'https://missav.ai/{request.state.lang}/playlists?page={page}'), headers=HEADERS,
        cookies=cookies, verify=False)
    if response.status_code == 200:
        tree = html.fromstring(response.text)
        parse_login(tree)
        ret = parse_playlists(tree)
        return BaseResponse(data=PageResult(current_page=page, page_size=ret[0], page_count=ret[1], data=ret[2]))


@app.get("/detail/{key}",
         response_model=BaseResponse,
         tags=["Playlist API"],
         summary="playlists detail info",
         description="get playlist detail info of user ")
async def playlists(request: Request, cookies: AuthKeyDepend,
                    key: str = Path(...,
                                    title="playlist key",
                                    description="set playlist key, return playlist detail info"), page: int = 1):
    response = requests.get(
        url=parse_url(f'https://missav.ai/{request.state.lang}/playlists/{key}?page={page}'), headers=HEADERS,
        cookies=cookies, verify=False)
    if response.status_code == 200:
        tree = html.fromstring(response.text)
        parse_login(tree)
        ret = parse_playlist_detail(tree)
        return BaseResponse(data=PageResult(current_page=page, page_size=ret[0], page_count=ret[1], data=ret[2]))


@app.post("",
          response_model=BaseResponse,
          tags=["Playlist API"],
          summary="create a playlists",
          description="create a playlists")
async def create_playlists(request: Request, cookies: AuthKeyDepend,
                           input: PlaylistInput):
    response = requests.post(
        url=parse_url(f'https://missav.ai/{request.state.lang}/playlists/create'), headers=HEADERS,
        json={
            "name": "wukong",
            "description": "this is test",
            "scope": 0
        },
        cookies=cookies, verify=False)
    if response.status_code == 200:
        return BaseResponse()
    return BaseResponse(success=False, code=response.status_code, message=response.text)


@app.delete("/{key}",
            response_model=BaseResponse,
            tags=["Playlist API"],
            summary="delete a playlist",
            description="delete a playlist")
async def delete_playlist(request: Request, cookies: AuthKeyDepend,
                          key: str):
    html_res = requests.get(
        url=parse_url(f'https://missav.ai/{request.state.lang}/playlists/{key}/edit'), headers=HEADERS,
        cookies=cookies, verify=False)
    if html_res.status_code == 200:
        tree = html.fromstring(html_res.text)
        parse_login(tree)
        ret = parse_playlist_delete_token(tree)

    response = requests.post(
        url=parse_url(f'https://missav.ai/{request.state.lang}/playlists/{key}'), headers=HEADERS,
        data={
            "_method": "delete",
            "_token": ret
        },
        cookies=cookies, verify=False)
    if response.status_code == 200:
        return BaseResponse()
    return BaseResponse(success=False, code=response.status_code, message=response.reason)


@app.delete("/{key}/{number}",
            response_model=BaseResponse,
            tags=["Playlist API"],
            summary="Remove an movie from the playlist",
            description="Remove an movie from the playlist")
async def remove_movie(request: Request, cookies: AuthKeyDepend,
                       key: str, number: str,):
    response = requests.delete(
        url=parse_url(f'https://missav.ai/api/playlists/{key}/{number}'), headers=HEADERS,
        cookies=cookies, verify=False)
    if response.status_code == 200:
        return BaseResponse()
    return BaseResponse(success=False, code=response.status_code, message=response.text)


@app.post("/comment/{key}/{number}",
          response_model=BaseResponse,
          tags=["Playlist API"],
          summary="comment a playlist",
          description="comment a playlist")
async def comment(request: Request, cookies: AuthKeyDepend, key: str, number: str,
                  comment: str):
    response = requests.post(
        url=parse_url(f'https://missav.ai/api/playlists/{key}/{number}/comment'), headers=HEADERS,
        json={
            "comment": comment
        },
        cookies=cookies, verify=False)
    if response.status_code == 200:
        return BaseResponse()
    return BaseResponse(success=False, code=response.status_code, message=response.text)
