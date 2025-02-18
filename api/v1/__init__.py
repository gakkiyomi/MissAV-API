

from fastapi import APIRouter

from api.v1.actress import app as actress_app
from api.v1.genres import app as genres_app
from api.v1.maker import app as maker_app
from api.v1.movie import app as movie_app
from api.v1.playlist import app as playlist_app
from api.v1.user import app as user_app

router = APIRouter(
    prefix='/api/v1'
)
router.include_router(user_app)
router.include_router(movie_app)
router.include_router(playlist_app)
router.include_router(actress_app)
router.include_router(genres_app)
router.include_router(maker_app)
