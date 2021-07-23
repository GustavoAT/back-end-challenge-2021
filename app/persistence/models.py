"""ORM-mapped objects.

    To use with sqlalchemy.orm
    """
from sqlalchemy import Column, Integer, String, Enum, Float
from sqlalchemy import DateTime, SmallInteger
from .database import Base
import enum




class GendersEnum(enum.Enum):
    male = enum.auto()
    female = enum.auto()


class StatusEnum(enum.Enum):
    draft = enum.auto()
    trash = enum.auto()
    published = enum.auto()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    gender = Column(Enum(GendersEnum))
    title = Column(String(4))
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    loc_street = Column(String(40))
    loc_city = Column(String(30))
    loc_state = Column(String(30))
    loc_postcode = Column(String(20))
    coordinates_latitude = Column(Float)
    coordinates_longitude = Column(Float)
    timezone_offset = Column(String(6))
    timezone_description = Column(String(20))
    email = Column(String(30), unique=True)
    login_uuid = Column(String(40), unique=True)
    login_username = Column(String(20), unique=True, nullable=False)
    login_password = Column(String(70), nullable=False)
    login_salt = Column(String(20), nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    age = Column(SmallInteger)
    registered_date = Column(DateTime)
    registered_age = Column(SmallInteger)
    phone = Column(String(15))
    cell = Column(String(15))
    id_name = Column(String(10))
    id_value = Column(String(20), unique=True)
    picture_large = Column(String(60))
    picture_medium = Column(String(60))
    picture_thumbnail = Column(String(60))
    nat = Column(String(2))
    imported_t = Column(DateTime, nullable=False)
    status = Column(Enum(StatusEnum), nullable=False)