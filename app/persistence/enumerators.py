from enum import Enum


class GendersEnum(str, Enum):
    male = 'male'
    female = 'female'


class StatusEnum(str, Enum):
    draft = 'draft'
    trash = 'trash'
    published = 'published'
