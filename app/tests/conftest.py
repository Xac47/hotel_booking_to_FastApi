import asyncio
import json
from datetime import date

import pytest
from bookings.models import Bookings
from hotels.models import Hotels, Rooms
from httpx import AsyncClient
from sqlalchemy import Delete, Insert
from users.models import Users

from app.config import settings
from app.database import Base, async_session_maker, engine


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    bookings = open_mock_json("bookings")
    hotels = open_mock_json("hotels")
    rooms = open_mock_json("rooms")
    users = open_mock_json("users")

    for booking in bookings:
        booking["date_from"] = date.fromisoformat(booking["date_from"])
        booking["date_to"] = date.fromisoformat(booking["date_to"])

    async with async_session_maker() as session:
        await session.execute(Delete(Bookings))
        await session.execute(Delete(Hotels))
        await session.execute(Delete(Rooms))
        await session.execute(Delete(Users))
        await session.commit()

        add_bookings = Insert(Bookings).values(bookings)
        add_hotels = Insert(Hotels).values(hotels)
        add_rooms = Insert(Rooms).values(rooms)
        add_users = Insert(Users).values(users)

        await session.execute(add_hotels)
        await session.execute(add_rooms)
        await session.execute(add_users)
        await session.execute(add_bookings)

        await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(base_url="http://localhost:8000/") as ac:
        yield ac


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session
