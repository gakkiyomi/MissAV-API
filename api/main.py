from fastapi import FastAPI

from api.common.logging import setup_logging
from api.common.middleware import register_middlewares
from api.v1 import router as v1_router

setup_logging()
misscore = FastAPI(
    title="misscore API docs",
    description="missav website backend api server",
    version="0.0.1"
)
register_middlewares(misscore)
misscore.include_router(v1_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(misscore, host="0.0.0.0", port=8000)
