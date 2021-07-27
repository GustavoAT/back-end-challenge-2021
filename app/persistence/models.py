"""ORM-mapped objects.

    To use with sqlalchemy.orm
    """
import sys
from sqlalchemy import Column, Integer, String, Enum, Float
from sqlalchemy import DateTime, SmallInteger
from .database import Base, engine
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
    name_title = Column(String(4))
    name_first = Column(String(30), nullable=False)
    name_last = Column(String(30), nullable=False)
    location_street = Column(String(40))
    location_city = Column(String(80))
    location_state = Column(String(40))
    location_postcode = Column(String(20))
    location_coordinates_latitude = Column(Float)
    location_coordinates_longitude = Column(Float)
    location_timezone_offset = Column(String(6))
    location_timezone_description = Column(String(80))
    email = Column(String(30), unique=True)
    login_uuid = Column(String(40), unique=True)
    login_username = Column(String(40), unique=True, nullable=False)
    login_password = Column(String(70), nullable=False)
    login_salt = Column(String(20), nullable=False)
    dob_date = Column(DateTime, nullable=False)
    dob_age = Column(SmallInteger)
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


def create_tables():
    Base.metadata.create_all(bind=engine)


def delete_tables():
    Base.metadata.drop_all(bind=engine)


if __name__ == '__main__':
    if sys.argv[1]:
        if sys.argv[1] == '-c':
            delete_tables()
            create_tables()
            print('Tabelas criadas')
    else:
        print('Este comando espera pelo menos um argumento')