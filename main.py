from fastapi import FastAPI
from DB_functions import Db
from Data_class import Data

db = Db()
app = FastAPI()


@app.post('/submitData')
async def submitData(data: Data):
    return db.submitdata(data)


@app.get("/")
async def root():
    print('success')


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

