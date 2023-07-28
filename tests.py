from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_POST_submit_data():
    """ Тест внесения данных. """
    response = client.post('/submitData', json={
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
    })
    assert response.status_code == 200


def test_GET_submitData():
    """ Тест запроса данных """
    response = client.get('/submitData/%3Cget_id%3E?get_id=3')
    assert response.status_code == 200
    assert response.json() == {
        "status": "new",
        "email": "string",
        "fam": "string",
        "name": "string",
        "oct": "string",
        "phone": 0,
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
        "img_1_title": None,
        "img_1_data": None,
        "img_2_title": None,
        "img_2_data": None
    }


def test_patch_submitData():
    """ Тест редактирования данных """
    response = client.patch('/submitData/%3Cpatch_id%3E?patch_id=3', json={
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
    })
    assert response.status_code == 200
    assert response.json() == {"state": 1, "message": None}


def test_patch_block_changing_user():
    """ Тест запрета редактирования данных пользователя """
    response = client.patch('/submitData/%3Cpatch_id%3E?patch_id=3', json={
        "beauty_title": "string",
        "title": "string",
        "other_titles": "string",
        "connect": "string",
        "user": {
            "email": "TEST",
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
    })
    assert response.status_code == 200
    assert response.json() == {"state": 0, "message": "Запрещено менять данные пользователя."}


def test_get_by_email():
    """ Тест поиска по email """
    response = client.get('/submitData/%3Cemail%3E?email=BIBA%40BIBA.ru')
    assert response.status_code == 200
    assert response.json() == {
        "status": 1,
        "data": {
            "root": [
                {
                    "id": 5,
                    "status": "new",
                    "beauty_title": "LAST_TEST",
                    "title": "string",
                    "others_titles": "LAST",
                    "connect": "string",
                    "date_added": "2023-07-28T12:49:48.993267",
                    "latitude": 1421.45,
                    "longitude": 12323.5,
                    "height": 900,
                    "img_0_title": "Подъем",
                    "img_0_data": "//fgfdgoruhushrtidhsuifuvilsdrbvrlizduhrtldxughlfjv",
                    "img_1_title": "Спуск",
                    "img_1_data": "//gdfujgheiohuhgufdhdufghxcho",
                    "img_2_title": None,
                    "img_2_data": None
                }
            ]
        }
    }


def test_get_by_email_user_not_found():
    response = client.get('/submitData/%3Cemail%3E?email=not%40found.ru')
    assert response.status_code == 200
    assert response.json() == {"status": 0, "message": "Пользователь не найден."}
