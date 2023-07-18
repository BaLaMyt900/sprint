from fastapi import FastAPI
from DB_functions import Db
from Data_class import Data, ResponsePerevalModel

db = Db()
app = FastAPI()


@app.post('/submitData', response_model=Data)
async def submitData(data: Data):
    """ ПОСТ запрос для добавления данных """
    return db.submitData(data)


@app.get('/submitData/<id>', response_model=ResponsePerevalModel)
async def getData(get_id: int):
    """ ГЕТ запрос данных из БД согласно форме для предоставления """
    return db.getData(get_id)


@app.patch('/submitData/<id>', response_model=Data)
async def patchData(patch_id: int, data: Data):
    return db.patchData(patch_id, data)