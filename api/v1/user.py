import logging

import requests
from fastapi import APIRouter

from api.common.constants import HEADERS
from api.domain.model import BaseResponse, UserInfo

logger = logging.getLogger(__name__)
app = APIRouter(
    prefix='/user',
)


@app.post("/login",
          response_model=BaseResponse,
          tags=["User API"],
          summary="user login",
          description="user login from missav")
async def login(user: UserInfo):
    response = requests.post(url='https://missav.ai/api/login',
                             data={'email': user.email, 'password': user.password}, headers=HEADERS, verify=False)
    if response.status_code == 200:
        cookie_info = response.cookies.get_dict()
        if "user_uuid" in cookie_info:
            cookie_str = "; ".join(
                [f"{key}={value}" for key, value in cookie_info.items()])
            return BaseResponse(data=cookie_str)
    return BaseResponse(success=False, code=response.status_code,
                        message="Login failed, check your network connection or account information.")
