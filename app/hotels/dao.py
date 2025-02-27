from datetime import date

from sqlalchemy import Select, and_, cte, func, label, or_

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotels, Rooms


class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_all_rooms(cls, hotel_id: int):
        async with async_session_maker() as session:
            """
            select * from rooms
            left join hotels on rooms.hotel_id=hotels.id
            where hotels.id = 1
            """
            query = (
                Select(Rooms)
                .join(cls.model, Rooms.hotel_id == cls.model.id, isouter=True)
                .where(cls.model.id == hotel_id)
            )

            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def search_to_location(cls, location: str):
        async with async_session_maker() as session:
            query = Select(cls.model).where(cls.model.location.contains(location.title()))

            result = await session.execute(query)

            return result.scalars().all()

    # @classmethod
    # async def search_for_hotels(cls, location: str, date_from: date, date_to: date):
        # """
        # SELECT hotel_id, hotels.rooms_quantity - count(anon_2.room_id) as rooms_left, hotels.r
        # LEFT OUTER JOIN rooms ON rooms. hotel_id = hotels.id
        # LEFT OUTER JOIN (
        # SELECT * FROM bookings
        # WHERE (date_from < '2023-02-15' AND date_to > '2023-02-15')
        # OR (date_from >= '2023-02-15' AND date_from < '2023-03-17')
        # ) AS anon_2
        # ON anon_2. room_id = rooms.id
        # WHERE (hotels. location LIKE 'Алтай')
        # GROUP BY hotel_id, hotels.rooms_quantity
        # """
        # async with async_session_maker() as session:
        #     bookings_for_selected_dates = (
        #         Select(cls.model)
        #         .filter(
        #             or_(
        #                 and_(
        #                     Bookings.date_from < date_from, Bookings.date_to > date_from
        #                 ),
        #                 and_(
        #                     Bookings.date_from >= date_from,
        #                     Bookings.date_from < date_to,
        #                 ),
        #             )
        #         )
        #         .subquery("filtered_bookings")
        #     )

        #     hotels_rooms_left = (
        #         Select(
        #             (
        #                 Hotels.rooms_quantity
        #                 - func.count(bookings_for_selected_dates.c.room_id)
        #             ).label("rooms_left"),
        #             Rooms.hotel_id,
        #         )
        #         .select_from(Hotels)
        #         .outerjoin(Rooms, Rooms.hotel_id == Hotels.id)
        #         .outerjoin(
        #             bookings_for_selected_dates,
        #             bookings_for_selected_dates.c.room_id == Rooms.id,
        #         )
        #         .where(
        #             Hotels.location.contains(location.title()),
        #         )
        #         .group_by(Hotels.rooms_quantity, Rooms.hotel_id)
        #         .cte("hotels_rooms_left")
        #     )

        #     get_hotels_info = (
        #         Select(
        #             Hotels.__table__.columns,  # Все колонки таблицы hotels
        #             hotels_rooms_left.c.rooms_left,  # Доп. колонка с количеством комнат
        #         )
        #         .select_from(Hotels)
        #         .join(hotels_rooms_left, hotels_rooms_left.c.hotel_id == Hotels.id)
        #         .where(hotels_rooms_left.c.rooms_left > 0)
        #     )

        #     hotels_info = await session.execute(get_hotels_info)
        #     return hotels_info.scalars().all()


class RoomsDAO(BaseDAO):
    model = Rooms
