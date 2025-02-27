from sqladmin import ModelView

from app.bookings.models import Bookings
from app.hotels.models import Hotels, Rooms
from app.users.models import Users


class UserAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email]
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    can_delete = False
    column_details_exclude_list = [Users.hashed_password]


class BookingAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.columns] + [Bookings.user]
    name = "Бронь"
    name_plural = "Брони"
    icon = "fa-solid fa-hotel"


class HotelAdmin(ModelView, model=Hotels):
    column_list = [c.name for c in Hotels.__table__.columns] + [Hotels.rooms]
    name = "Отель"
    name_plural = "Отели"
    icon = "fa-solid fa-hotel"


class RoomAdmin(ModelView, model=Rooms):
    column_list = [c.name for c in Rooms.__table__.columns] + [Rooms.hotel]
    name = "Комната"
    name_plural = "Комнаты"
    icon = "fa-solid fa-bed"
