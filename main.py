import json
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union
from DB_functions import Db

db = Db()
app = FastAPI()


class Data(BaseModel):
    beauty_title: str
    title: str
    other_titles: str
    connect: Union[str, None] = None




@app.post('/submitData')
async def submitData(data: json):
    db.submitdata(data)
    return data


@app.get("/")
async def root():
    print('success')


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

