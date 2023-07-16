from pydantic import BaseModel, RootModel
from typing import Union, List


class User(BaseModel):
    """ Класс данных пользователя """
    email: str
    fam: str
    name: str
    oct: str
    phone: int


class Coords(BaseModel):
    """ Класс данных координат """
    latitude: float
    longitude: float
    height: int


class Level(BaseModel):
    """ Класс данных уровня сложности """
    winter: str
    summer: str
    autumn: str
    spring: str


class Image(BaseModel):
    """ Класс данных одной картинки """
    data: bytes
    title: str


class Images(RootModel):
    """ Класс запроса ЛИСТА картинок """
    root: List[Image]


class Data(BaseModel):
    """ Класс данных, принимаемых при submitData """
    beauty_title: str
    title: str
    other_titles: str
    connect: Union[str, None] = None
    user: User
    coords: Coords
    level: Level
    images: Images

