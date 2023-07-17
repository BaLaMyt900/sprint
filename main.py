from fastapi import FastAPI
from DB_functions import Db
from Data_class import Data, ResponsePerevalModel
from fastapi.responses import JSONResponse

db = Db()
app = FastAPI()


@app.post('/submitData', response_model=Data)
async def submitData(data: Data):
    """ ПОСТ запрос для добавления данных """
    return JSONResponse(db.submitData(data))


@app.get('/submitData/<id>', response_model=ResponsePerevalModel)
async def getData(get_id: int):
    """ ГЕТ запрос данных из БД согласно форме для предоставления """
    data = db.getData(get_id)
    if data:  # if для транформации memoryview из БД в bytea для модели
        return ResponsePerevalModel(**{key: data[i].tobytes() if isinstance(data[i], memoryview) else data[i]
                                       for i, key in enumerate(ResponsePerevalModel.model_fields.keys())})
    else:
        return JSONResponse({'status': 204, 'message': 'Данные не найдены.'})
