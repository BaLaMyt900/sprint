## Спринт

### Реализация API сервера согласно тех. заданию от SkillFactory.

Библиотеки:
- FastAPI
- uvicorn
- psycopg2
- pydantic

Swagger доступен по пути: http://127.0.0.1:8000/docs#/<br>
Тестовый сервер размещен по адресу: http://185.139.70.198:8080/docs#
### Реализованные методы:
 
#### POST: /submitData
Метод внесения данных в базу. Принимает фотографии списком, максимум 3.<br>
Автоматически присваеивает дату и статус NEW.<br>
Пример из Swagger
```json
{
  "beauty_title": "string",
  "title": "string",
  "other_titles": "string",
  "connect": "string",
  "user": {
    "email": "string",
    "fam": "string",
    "name": "string",
    "oct": "string",
    "phone": 0
  },
  "coords": {
    "latitude": 0,
    "longitude": 0,
    "height": 0
  },
  "level": {
    "winter": "string",
    "summer": "string",
    "autumn": "string",
    "spring": "string"
  },
  "images": [
    {
      "data": "string",
      "title": "string"
    }
  ]
}
```

#### GET /submitData/id
Запрос информации из бд по ид согласно форме. Пример
```json
{
  "status": "new",
  "email": "qwerty@mail.ru",
  "fam": "Пупкин",
  "name": "Василий",
  "oct": "Иванович",
  "phone": 75555555,
  "beauty_title": "пер. ",
  "title": "Пхия",
  "others_titles": "Триев",
  "connect": "",
  "date_added": "2023-07-17T13:19:22.433645",
  "latitude": 45.3842,
  "longitude": 7.1525,
  "height": 1200,
  "img_0_title": "Седловина",
  "img_0_data": "\\x89504e470d0a1a0a0000...", 
  "img_1_title": null,
  "img_1_data": null,
  "img_2_title": null,
  "img_2_data": null
}
```

#### PATCH /submitData/id
Метод обновления записи. Требует ИД записи и JSON данные в форме аналогично вводу.<br>
Ограничения: Запись должна быть в статусе NEW, запрещено менять данные пользователя.

#### GET /submitData/?email=email
Метод получения списка данных, отправленных пользователем. 
Пример полученных данных:
```json
{
  "status": 1,
  "data": {
    "root": [
      {
        "id": 3,
        "status": "new",
        "beauty_title": "string",
        "title": "string",
        "others_titles": "string",
        "connect": "string",
        "date_added": "2023-07-28T07:33:20.826065",
        "latitude": 0,
        "longitude": 0,
        "height": 0,
        "img_0_title": "string",
        "img_0_data": "string",
        "img_1_title": null,
        "img_1_data": null,
        "img_2_title": null,
        "img_2_data": null
      }
    ]
  }
}
```
