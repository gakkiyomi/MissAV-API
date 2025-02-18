from typing import List, Tuple

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

translations = {
    "us": "en",
    "en": "en",
    "en-US": "en",
    "en_US": "en",
    "en-UK": "en",
    "en_UK": "en",
    "zh_HK": "",
    "zh-HK": "",
    'hk': "",
    "zh-TW": "",
    "zh_TW": "",
    "zh_CN": "cn",
    "zh-CN": "cn",
    "zh": "cn",
    "cn": "cn",
    "ja": "ja",
    "ko": "ko",
    "kr": "ko",
    "ms": "ms",
    "th": "th",
    "de": "de",
    "fr": "fr",
    "vi": "vi",
    "id": "id",
    "fil": "fil",
    "pt_BR": "pt",
    "pt": "pt"
}


# 中间件实现
class LanguageMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        accept_language = request.headers.get(
            "accept-language", translations['en'])
        # 将语言存储在请求上下文中
        request.state.lang = self.select_language(
            self.parse_accept_language(accept_language))
        response = await call_next(request)
        response.headers["Content-Language"] = request.state.lang
        return response

    def parse_accept_language(self, header: str) -> List[Tuple[str, float]]:
        """解析 Accept-Language 头部，返回排序后的语言列表"""
        langs = []
        for part in header.split(","):
            lang_part = part.split(";")[0].strip()
            q = 1.0
            if "q=" in part:
                q = float(part.split("q=")[1].split(",")[0])
            langs.append((lang_part, q))
        if langs:
            # 按权重降序排序
            langs.sort(key=lambda x: x[1], reverse=True)
        return langs

    def select_language(self, langs: List[Tuple[str, float]]) -> str:
        if langs:
            return translations.get(langs[0][0], translations['en'])
        return translations['en']


def register_middlewares(app: FastAPI):
    app.add_middleware(CORSMiddleware,
                       allow_origins=["*"],
                       allow_credentials=["*"],
                       allow_methods=["*"],
                       allow_headers=["*"])
    app.add_middleware(LanguageMiddleware)
