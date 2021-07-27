"""Pydantic mapped objects.

    Make it easy to map dictionaries and orm objects to pythonic objects.
    """
from datetime import datetime
from typing import Optional
from pydantic import BaseModel




class UserBase(BaseModel):
    gender: str
    name_title: Optional[str] = None
    name_first: Optional[str] = None
    name_last: Optional[str] = None
    location_street: Optional[str] = None
    location_city: Optional[str] = None
    location_state: Optional[str] = None
    location_postcode: Optional[str] = None
    location_coordinates_latitude: Optional[float] = None
    location_coordinates_longitude: Optional[float] = None
    location_timezone_offset: Optional[str] = None
    location_timezone_description: Optional[str] = None
    email: str
    login_uuid: str
    login_username: str
    dob_date: datetime
    dob_age: Optional[int] = None
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
    status: str = 'draft'


class UserCreate(UserBase):
    login_password: str
    login_salt: Optional[str] = None


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
        