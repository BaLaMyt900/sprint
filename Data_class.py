from pydantic import BaseModel, RootModel
from typing import Union, List, Optional
from datetime import datetime


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
    """ Класс данных уровня сложности. Заполняется метками класса опастности.
    От А1(Самый сложный) до Г5(Очень простой) """
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


class ResponsePerevalModel(BaseModel):
    """ Класс модуля предоставления данных для ГЕТ запроса """
    status: str
    email: str
    fam: str
    name: str
    oct: str
    phone: int
    beauty_title: str
    title: str
    others_titles: str
    connect: str
    date_added: datetime = None
    latitude: float
    longitude: float
    height: int
    img_0_title: Optional[str] = None
    img_0_data: Optional[bytes] = None
    img_1_title: Optional[str] = None
    img_1_data: Optional[bytes] = None
    img_2_title: Optional[str] = None
    img_2_data: Optional[bytes] = None


class ResponsePerevalModelByAll(BaseModel):
    id: int
    status: str
    email: str
    fam: str
    name: str
    oct: str
    phone: int
    beauty_title: str
    title: str
    others_titles: str
    connect: str
    date_added: datetime = None
    latitude: float
    longitude: float
    height: int
    img_0_title: Optional[str] = None
    img_0_data: Optional[bytes] = None
    img_1_title: Optional[str] = None
    img_1_data: Optional[bytes] = None
    img_2_title: Optional[str] = None
    img_2_data: Optional[bytes] = None


class ResponsePerevalModelByList(BaseModel):
    root: List[ResponsePerevalModelByAll]


class ResponsePerevalByEmail(BaseModel):
    """ Модель запроса по email пользователя """
    id: int
    status: str
    beauty_title: str
    title: str
    others_titles: str
    connect: str
    date_added: datetime = None
    latitude: float
    longitude: float
    height: int
    img_0_title: Optional[str] = None
    img_0_data: Optional[bytes] = None
    img_1_title: Optional[str] = None
    img_1_data: Optional[bytes] = None
    img_2_title: Optional[str] = None
    img_2_data: Optional[bytes] = None


class ResponsePerevalByEmailList(BaseModel):
    """ Лист моделей полученных при поиске по email """
    root: List[ResponsePerevalByEmail]


class OnlyErrorModel(BaseModel):
    error: str
