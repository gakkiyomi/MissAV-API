from http.cookies import SimpleCookie
from typing import Annotated

from fastapi import Depends, Header, HTTPException


async def get_auth_key(
    auth_key: Annotated[str | None, Header()] = None
):
    if not auth_key:
        raise HTTPException(status_code=401, detail='Unauthorized')
    try:
        # 解析 cookie 字符串
        cookie = SimpleCookie(auth_key)
        cookie_dict = {key: morsel.value for key, morsel in cookie.items()}
        return cookie_dict
    except Exception as e:
        raise HTTPException(status_code=401, detail='Invalid auth key')

AuthKeyDepend = Annotated[dict, Depends(get_auth_key)]
