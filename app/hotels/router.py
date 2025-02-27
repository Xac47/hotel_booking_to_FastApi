from typing import Optional

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.hotels.dao import HotelsDAO
from app.hotels.shemas import SHotel, SRoom

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=20)
async def list_hotels(location: Optional[str] = None) -> list[SHotel]:
    result = await HotelsDAO.find_all()
    if location:
        result = await HotelsDAO.search_to_location(location=location)
    return result


# @router.get("/{location}")
# async def get__hotels_by_location_and_time(
#     location: str,
#     date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
#     date_to: date = Query(..., description=f"Например, {datetime.now().date()}"),
# ) -> list[SHotel]:
#     hotels = HotelsDAO.search_for_hotels(location, date_from, date_to)
#     return hotels


@router.get("/{hotel_id}/rooms")
async def get_rooms_hotel(hotel_id: int) -> list[SRoom]:
    result = await HotelsDAO.find_all_rooms(hotel_id)
    return result


@router.get("/id/{hotel_id}")
async def get_hotel(hotel_id: int):
    return await HotelsDAO.find_by_id(hotel_id)
