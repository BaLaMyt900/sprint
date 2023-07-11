from fastapi import FastAPI
from DB_functions import db_init

app = FastAPI()


@app.post('/submitData')
async def submitData(data):
    print(data)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

db_init()
