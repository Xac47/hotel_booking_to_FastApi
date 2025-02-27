from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin

from fastapi_versioning import VersionedFastAPI

from app.admin.auth import authentication_backend
from app.admin.views import BookingAdmin, HotelAdmin, RoomAdmin, UserAdmin
from app.bookings.router import router as router_bookings
from app.config import settings
from app.database import engine
from app.hotels.router import router as router_hotels
from app.images.router import router as router_images
from app.pages.router import router as router_pages
from app.users.router import router as router_users
from app.logger import logger

# REDIS


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


# END REDIS

app = FastAPI(lifespan=lifespan)


# ROUTER

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)

app.include_router(router_pages)
app.include_router(router_images)

# END ROUTER


origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "РАТСН", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin" "Authorization",
        "Authorization",
    ],
)

# VersionedFastAPI

app = VersionedFastAPI(
    app,
    version_format="{major}",
    prefix_format="/v{major}",
    # description="Greet users with a nice message",
    # middleware=[Middleware(SessionMiddleware, secret_key="mysecretkey")],
)

# END VersionedFastAPI

# ADMIN PANEL

admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UserAdmin)
admin.add_view(BookingAdmin)
admin.add_view(HotelAdmin)
admin.add_view(RoomAdmin)

# END ADMIN PANEL


# MIDDLEWARE


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    logger.info("Request handling time", extra={"process_time": round(process_time, 4)})
    return response


# END MIDDLEWARE


# STATIC

app.mount(
    "/static", StaticFiles(directory="app/static"), "static"
)  # примонтировали отдельную приложение, и по адрессу /static будет контент

# END STATIC
