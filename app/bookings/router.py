from datetime import date

from fastapi import APIRouter, Depends, Response, status
from fastapi_cache.decorator import cache
from pydantic import parse_obj_as
from fastapi_versioning import version

from app.bookings.dao import BookingDAO
from app.bookings.shemas import SBooking
from app.exceptions import RoomCannotBeBooked
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронированния"],
)


@version(1)
@router.get("")
@cache(expire=20)
async def user_list_bookings(user: Users = Depends(get_current_user)):
    return await BookingDAO.find_all_user_bookings(user_id=user.id)


@version(1)
@router.get("/{booking_id}")
async def get_booking(booking_id: int) -> SBooking:
    result = await BookingDAO.find_by_id(booking_id)
    return result


@version(1)
@router.post("/add")
async def create_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.create(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked()
    booking_dict = parse_obj_as(SBooking, booking).dict()
    send_booking_confirmation_email.delay(booking_dict, user.email)

    return booking


@version(1)
@router.delete("/{booking_id}/delete")
async def delete_booking(responce: Response, booking_id: int):
    await BookingDAO.delete(booking_id)
    res = responce.status_code = status.HTTP_204_NO_CONTENT
    return res
