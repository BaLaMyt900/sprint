from fastapi import FastAPI
from DB_functions import Db
from Data_class import Data, ResponsePerevalModel, ResponsePerevalByEmailList

db = Db()
app = FastAPI()


@app.post('/submitData', response_model=Data)
async def submitData(data: Data):
    """ Добавление данных в базу. Автоматически добавляет время и статус.
     Если пользователь новый, то его так же добаляет в базу."""
    return db.submitData(data)


@app.get('/submitData/{get_id}', response_model=ResponsePerevalModel)
async def getData(get_id: int):
    """ Запрос данных из базы. Необходим ID записи.
    Предоставляет информацию согласно форме, с отображением времени и статуса. """
    return db.getData(get_id)


@app.patch('/submitData/{patch_id}', response_model=Data)
async def patchData(patch_id: int, data: Data):
    """ Обновление записи базы данных. Запрашивает ID изменяемой записи и данные,
     согласно форме добаления.
     Запрещено менять данные пользователя, Запрещено менять данные, если статус не NEW"""
    return db.patchData(patch_id, data)


@app.get('/submitData/user_email={email}', response_model=ResponsePerevalByEmailList)
async def getForEmail(email: str):
    """ Поиск и получение данных по email-адресу пользователя.
    Отработаны ошибки о ненахождении пользователя и данных."""
    return db.getByEmail(email)
