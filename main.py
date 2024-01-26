from fastapi import FastAPI
from DB_functions import Db
from Data_class import Data, ResponsePerevalModel, ResponsePerevalByEmailList, ResponsePerevalModelByList, \
    OnlyErrorModel
from fastapi.responses import JSONResponse


db = Db()
app = FastAPI(
    title='TestCase',
    description="""Документация для тестового задания. API для взаимодействия с базой данных перевалов."""
)


@app.post('/submitData', response_model_exclude_unset=True, responses={
    200: {'description': 'Данные успешно добавлены в базу. Возвращен ИД номер записи.', "content": {}},
    400: {'description': 'Неправильные данные. Расшифровка в ответе.', 'model': OnlyErrorModel},
    401: {'description': 'Не обнаружены требуемые параметры.'},
    422: {'description': 'Ошибка валидации', 'content': ''}})
async def submit_data(data: Data):
    """ Добавление данных в базу. Автоматически добавляет время и статус.
     Если пользователь новый, то его так же добаляет в базу.
    latitude, longtitude - float."""
    if not data:
        return JSONResponse(None, 401)
    return db.submitData(data)


@app.get('/submitData', response_model_exclude_unset=True, responses={
    200: {'description': 'Данные получены.', 'model': ResponsePerevalModelByList},
    404: {'description': 'Данные не найдены.'},
    422: {'description': 'Ошибка валидации', 'content': ''}})
async def get_data():
    """ Получение всех записей из базы данных """
    return db.get_data()


@app.get('/submitData/<get_id>', response_model_exclude_unset=True, responses={
    200: {'description': 'Данные получены.', 'model': ResponsePerevalModel},
    400: {'description': 'Не обнаружены требуемые параметры.'},
    404: {'description': 'Данные не найдены.'},
    422: {'description': 'Ошибка валидации', 'content': ''}})
async def get_data_by_id(get_id: int):
    """ Запрос данных из базы. Необходим ID записи.
    Предоставляет информацию согласно форме, с отображением времени и статуса. """
    if not get_id:
        return JSONResponse(None, 400)
    return db.get_data_by_id(get_id)


@app.get('/submitData/<user_email>', response_model_exclude_unset=True, responses={
             200: {'model': ResponsePerevalByEmailList},
             400: {'description': 'Не обнаружены требуемые параметры.'},
             404: {'description': 'Пользователь либо данные не найдены.'},
             422: {'description': 'Ошибка валидации', 'content': ''}})
async def get_data_by_email(user_email: str):
    """ Поиск и получение данных по email-адресу пользователя.
    Отработаны ошибки о ненахождении пользователя и данных."""
    if not user_email:
        return JSONResponse(None, 400)
    return db.get_data_by_email(user_email)


@app.patch('/submitData/<patch_id>', response_model_exclude_unset=True, responses={
    200: {'description': 'Данные обновлены.', 'content': None},
    400: {'description': 'Не обнаружены требуемые параметры.'},
    404: {'description': 'Данные не найдены.', 'content': None},
    422: {'description': 'Ошибка валидации', 'content': ''}
})
async def patch_data(patch_id: int, data: Data):
    """ Обновление записи базы данных. Запрашивает ID изменяемой записи и данные,
     согласно форме добаления.
     Запрещено менять данные пользователя, Запрещено менять данные, если статус не NEW"""
    if not patch_id or not data:
        return JSONResponse(None, 400)
    return db.patchData(patch_id, data)


@app.delete('/submitData/<user_email>/<id>', response_model_exclude_unset=True, responses={
    200: {'description': 'Запрос обработан.', 'content': None},
    400: {'description': 'Не обнаружены требуемые параметры.'}
})
async def delete_data(user_email: str, id: int):
    """ Удаление записи. Принимает почту и ид записи. """
    if not user_email or not id:
        return JSONResponse(None, 400)
    return db.deleteData(user_email, id)


