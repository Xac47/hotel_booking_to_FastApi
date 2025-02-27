from datetime import date

from sqlalchemy import Insert, Select, and_, func, or_
from sqlalchemy.exc import SQLAlchemyError

from app.logger import logger
from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Rooms
from app.users.models import Users


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def create(cls, user_id: int, room_id: int, date_from: date, date_to: date):
        try:
            async with async_session_maker() as session:

                """
                with booked_rooms as (
                select * from bookings
                where room_id = 1 and
                (date_from >= '2023-05-15' and date_from <= '2023-06-20') or
                (date_from <= '2023-05-15' and date_to > '2023-05-15')
                )
                """
                booked_rooms = (
                    Select(cls.model)
                    .where(
                        and_(
                            cls.model.room_id == room_id,
                            or_(
                                and_(
                                    cls.model.date_from >= date_from,
                                    cls.model.date_from <= date_to,
                                ),
                                and_(
                                    cls.model.date_from <= date_from,
                                    cls.model.date_to > date_from,
                                ),
                            ),
                        )
                    )
                    .cte("booked_rooms")
                )
                """
                select rooms.quantity - count(booked_rooms.room_id) from rooms
                left join booked_rooms on booked_rooms.room_id = rooms.id
                where rooms.id = 1
                group by rooms.quantity, booked_rooms.room_id
                """

                get_rooms_left = (
                    (
                        Select(
                            (Rooms.quantity - func.count(booked_rooms.c.room_id)).label(
                                "rooms_left"
                            )
                        )
                        .select_from(Rooms)
                        .join(
                            booked_rooms,
                            booked_rooms.c.room_id == Rooms.id,
                            isouter=True,
                        )
                    )
                    .where(Rooms.id == room_id)
                    .group_by(Rooms.quantity, booked_rooms.c.room_id)
                )

                rooms_left = await session.execute(get_rooms_left)
                rooms_left: int = rooms_left.scalar()

                if not rooms_left or rooms_left > 0:
                    get_price = Select(Rooms.price).filter_by(id=room_id)
                    price = await session.execute(get_price)
                    price: int = price.scalar()
                    add_booking = (
                        Insert(Bookings)
                        .values(
                            room_id=room_id,
                            user_id=user_id,
                            date_from=date_from,
                            date_to=date_to,
                            price=price,
                        )
                        .returning(Bookings)
                    )
                    new_booking = await session.execute(add_booking)
                    await session.commit()
                    return new_booking.scalar()
                else:
                    return None
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot add booking"

            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot add booking"
            extra = {
                "user_id": user_id,
                "room_id": room_id,
                "date_from": date_from,
                "date_to": date_to,
            }
            logger.error(msg, extra=extra, exc_info=True )

    @classmethod
    async def find_all_user_bookings(cls, user_id: int):
        async with async_session_maker() as session:
            """
            select bookings.*, rooms.image_id, rooms.name, rooms.description, rooms.services from bookings
            left join users on bookings.user_id=users.id
            left join rooms on bookings.room_id=rooms.id
            where users.id = 3

            """
            query = (
                Select(
                    cls.model,
                    Rooms.image_id,
                    Rooms.name,
                    Rooms.description,
                    Rooms.services,
                )
                .join(Users, cls.model.user_id == Users.id)
                .join(Rooms, cls.model.room_id == Rooms.id)
                .where(cls.model.user_id == user_id)
            )

            result = await session.execute(query)

            return result.scalars().all()
