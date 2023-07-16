from fastapi import FastAPI
from DB_functions import Db
from Data_class import Data
from fastapi.responses import JSONResponse


db = Db()
app = FastAPI()


@app.post('/submitData', response_model=Data)
async def submitData(data: Data):
    return JSONResponse(db.submitdata(data))
