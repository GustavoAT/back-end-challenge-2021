"""Pydantic mapped objects.

    Make it easy to map dictionaries and orm objects to pythonic objects.
    """
from datetime import datetime
from typing import Optional
from pydantic import BaseModel




class UserBase(BaseModel):
    gender: str
    title: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    loc_street: Optional[str] = None
    loc_city: Optional[str] = None
    loc_state: Optional[str] = None
    loc_postcode: Optional[str] = None
    coordinates_latitude: Optional[float] = None
    coordinates_longitude: Optional[float] = None
    timezone_offset: Optional[str] = None
    timezone_description: Optional[str] = None
    email: str
    login_uuid: str
    login_username: str
    date_of_birth: datetime
    age: Optional[int] = None
    registered_date: Optional[datetime] = None
    registered_age: Optional[int] = None
    phone: Optional[str] = None
    cell: Optional[str] = None
    id_name: Optional[str] = None
    id_value: Optional[str] = None
    picture_large: Optional[str] = None
    picture_medium: Optional[str] = None
    picture_thumbnail: Optional[str] = None
    nat: Optional[str] = None
    imported_t: datetime
    status: str


class UserCreate(UserBase):
    login_password: str
    login_salt: Optional[str] = None


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
        