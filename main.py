from fastapi import FastAPI
from DB_functions import Db
from Data_class import Data, ResponsePerevalModel
from fastapi.responses import JSONResponse

db = Db()
app = FastAPI()


@app.post('/submitData', response_model=Data)
async def submitData(data: Data):
    return JSONResponse(db.submitData(data))


@app.get('/submitData/<id>', response_model=ResponsePerevalModel)
async def getData(get_id: int):
    data = db.getData(get_id)
    return ResponsePerevalModel(**{key: data[i].tobytes() if isinstance(data[i], memoryview) else data[i]
                                   for i, key in enumerate(ResponsePerevalModel.model_fields.keys())})
