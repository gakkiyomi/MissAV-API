
from typing import Any

from pydantic import BaseModel, Field


class UserInfo(BaseModel):
    email: str = Field(..., example="xxx@gmail.com", description="email")
    password: str = Field(..., example="xxxxx", description="password")


class PlaylistInput(BaseModel):
    name: str = Field(..., example="wukong", description="playlist name")
    description: str = Field(..., example="this is test",
                             description="playlist description")
    scope: int = 0


class PageResult(BaseModel):
    current_page: int = Field(..., example=1,
                              description="currentm page index")
    page_size: int = Field(..., example=12,
                           description="number of entries per page")
    page_count: int = Field(..., example=12,
                            description="total number of pages")
    data: Any = Field(..., example=[], description="data list")


class BaseResponse(BaseModel):
    code: int = 0
    success: bool = True
    message: str = "ok"
    data: Any = None
