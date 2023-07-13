import datetime
import json

import timestamp as timestamp
from fastapi import FastAPI
from pydantic import BaseModel, Json
from typing import Union
from DB_functions import Db

db = Db()
app = FastAPI()


class Data(BaseModel):
    beauty_title: str
    title: str
    other_titles: str
    connect: Union[str, None] = None
    add_time: datetime.datetime
    user: dict
    coords: dict
    level: dict
    images: list



@app.post('/submitData')
async def submitData(data: Json):  # TODO Явно обозначить JSON формат данных
    # db.submitdata(data)
    return type(data)


@app.get("/")
async def root():
    print('success')


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

