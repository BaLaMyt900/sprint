import sqlite3
from Data_class import Data, ResponsePerevalModel, ResponsePerevalByEmail, ResponsePerevalByEmailList, \
    ResponsePerevalModelByAll, ResponsePerevalModelByList
from DB_Requests import *
from fastapi.responses import JSONResponse


class Db:
    """ Класс для работы с базой данных """

    def __init__(self):
        """ Создание таблиц в базе данных """
        self.makeConnection()

        """ Создание таблицы Users """
        self.cur.execute(ADD_USERS)
        self.conn.commit()

        """ Создание таблицы Coords """
        self.cur.execute(ADD_COORDS)
        self.conn.commit()

        """ Создание таблицы pereval_images """
        self.cur.execute(ADD_IMAGES)
        self.conn.commit()

        """ Создание таблицы pereval_added """
        self.cur.execute(ADD_DATA)
        self.conn.commit()

        self.stopConnection()

    def makeConnection(self):
        """ Функция создания соединения с базой данных"""
        self.conn = sqlite3.connect('my_db.db')
        self.cur = self.conn.cursor()

    def stopConnection(self):
        """ Функция разрыва соединения с базой данных """
        self.cur.close()
        self.conn.close()

    def submitData(self, data: Data):
        """ Принятие новых данных """

        self.makeConnection()

        # Добавление фотографий

        images_id = []
        if data.images.root:
            if len(data.images.root) > 3:
                return JSONResponse({'error': 'Слишком много фотографий. Максимально 3.'}, 400)
            for image in data.images.root:
                self.cur.execute(INSERT_IMAGE,
                                 (image.title, image.data,))
                self.conn.commit()
                images_id.append(self.cur.lastrowid)

        # Добавление координат

        self.cur.execute(INSERT_COORDS,
                         (data.coords.latitude, data.coords.longitude, data.coords.height))
        self.conn.commit()
        coords_id = self.cur.lastrowid

        # Поиск  пользователя

        self.cur.execute(SELECT_USER_BY_EMAIL, (data.user.email,))
        self.conn.commit()
        user_id = self.cur.fetchone()

        # Добавление информации в pereval_added
        if user_id:  # Если пользователь найден, добавление с имеющимся ИД пользователя
            if user_id[0]:
                self.cur.execute(INSERT_DATA,
                                 (data.beauty_title, data.title, data.other_titles,
                                  data.connect, user_id[0],
                                  coords_id))
                self.conn.commit()
                object_id = self.cur.lastrowid
        else:  # Иначе добавление пользователя а потом уже информации
            try:
              self.cur.execute(INSERT_USER,
                               (data.user.email, data.user.phone, data.user.fam, data.user.name, data.user.oct))
            except sqlite3.IntegrityError:
              return JSONResponse({'error': 'Указанный номер уже записан под другим пользователем.'}, 400)
            self.conn.commit()
            user_id = self.cur.lastrowid
            self.cur.execute(INSERT_DATA,
                             (data.beauty_title, data.title, data.other_titles,
                              data.connect, user_id, coords_id,))
            self.conn.commit()
            object_id = self.cur.lastrowid

        if images_id:
            for img_id, image_id in enumerate(images_id):
                self.cur.execute(UPDATE_DATA_ADD_IMAGE_BY_IMG_ID % f'image_{img_id}', (image_id, object_id))
                self.conn.commit()

        self.stopConnection()

        return JSONResponse({'id': object_id}, 200)

    def get_data(self):
        self.makeConnection()
        self.cur.execute(SELECT_DATA_ALL)
        self.conn.commit()
        data = self.cur.fetchall()
        self.stopConnection()
        if not data:
            return JSONResponse({}, 404)
        output_data = []
        for item in data:
            output_data.append({key: item[i].tobytes() if isinstance(item[i], memoryview) else item[i]
                                for i, key in enumerate(ResponsePerevalModelByAll.model_fields.keys())})
        return JSONResponse(ResponsePerevalModelByList(root=output_data).model_dump(mode='json')['root'], 200)

    def get_data_by_id(self, data_id: int):
        """ Функция получения данных из базы """
        self.makeConnection()
        self.cur.execute(SELECT_DATA_BY_ID_FOR_GET_REQUEST, (data_id,))
        data = self.cur.fetchone()
        self.stopConnection()

        if data:  # if для транформации memoryview из БД в bytea для модели
            print(data)
            return JSONResponse(
                ResponsePerevalModel(**{key: data[i].tobytes() if isinstance(data[i], memoryview) else data[i]
                                        for i, key in enumerate(ResponsePerevalModel.model_fields.keys())}).model_dump(mode='json'), 200)
        else:
            return JSONResponse(None, 404)

    def get_data_by_email(self, email: str):
        """ Получение данных по email пользователя. """
        self.makeConnection()

        self.cur.execute(SELECT_USER_BY_EMAIL, (email,))
        user_id = self.cur.fetchone()
        if user_id:
            if not user_id[0]:
                """ Проверка нахождения пользователя """
                return JSONResponse(None, 404)
        else:
            return JSONResponse({'error': 'Пользователь не найден.'}, 400)
        self.cur.execute(SELECT_DATA_FOR_SEARCH_BY_USER_ID, (user_id[0],))
        data_list = self.cur.fetchall()
        self.stopConnection()
        if not data_list:
            """ Проверка наличия выходных данных """
            return JSONResponse(None, 404)
        output_data = []
        for item in data_list:
            output_data.append({key: item[i].tobytes() if isinstance(item[i], memoryview) else item[i]
                                for i, key in enumerate(ResponsePerevalByEmail.model_fields.keys())})
        return JSONResponse({'status': 1, 'data': ResponsePerevalByEmailList(root=output_data).model_dump(mode='json')})

    def _updatePhoto(self, img_id: int, old_title: str, old_data: bytes, new_title: str, new_data: bytes):
        """ Внутренний метод сравнения и обновления фотографий. """
        if all([img_id, any([old_title != new_title, old_data != new_data])]):
            self.cur.execute(UPDATE_PHOTO_FOR_PATCH, (new_title, new_data, img_id))
            return img_id
        elif not img_id:
            self.cur.execute(INSERT_IMAGE, (new_title, new_data))
            return self.cur.lastrowid

    def patchData(self, patch_id: int, data: Data):
        """ Функция редактирования данных.
         Условия: Данные находятся в статусе - new,
         Нельзя редактировать пользователя"""

        self.makeConnection()

        self.cur.execute(SELECT_DATA_FOR_PATCH, (patch_id,))
        oldData = self.cur.fetchone()
        if oldData:
            if oldData[0] != 'new':
                """ Проверка на статус 'Новый' """
                return JSONResponse({'state': 0, 'message': 'Запрещено изменять провернные данные.'}, 200)
            elif any([oldData[1] != data.user.email, oldData[2] != data.user.name, oldData[3] != data.user.fam,
                      oldData[4] != data.user.oct, oldData[5] != data.user.phone]):
                """ Проверка на соответсвие данных пользователя. """
                return JSONResponse({'state': 0, 'message': 'Запрещено менять данные пользователя.'}, 200)
        else:
            """ Проверка нахождения данных по id """
            return JSONResponse(None, 404)
        """ Обновление названия данных """
        if any([oldData[7] != data.coords.latitude,
                oldData[8] != data.coords.longitude, oldData[9] != data.coords.height]):
            """ Проверка и изменение кординат """
            self.cur.execute(UPDATE_COORDS_FOR_PATCH, (data.coords.latitude, data.coords.longitude,
                                                       data.coords.height, oldData[6]))
        """ Провека и изменение фотографий без изменения даты """
        # Первая фотография
        img_0 = oldData[10]
        try:
            if data.images.root[0]:
                img_0 = self._updatePhoto(img_0, oldData[11], oldData[12],
                                          data.images.root[0].title, data.images.root[0].data)
        except IndexError:
            pass

        # Вторая фотография
        img_1 = oldData[13]
        try:
            if data.images.root[1]:
                img_1 = self._updatePhoto(img_1, oldData[14], oldData[15],
                                          data.images.root[1].title, data.images.root[1].data)
        except IndexError:
            pass

        # Третья фотография
        img_2 = oldData[16]
        try:
            if data.images.root[2]:
                img_2 = self._updatePhoto(img_2, oldData[17], oldData[18],
                                          data.images.root[2].title, data.images.root[2].data)
        except IndexError:
            pass

        self.cur.execute(UPDATE_DATA_FOR_PATCH, (data.beauty_title, data.title,
                                                 data.other_titles, data.connect,
                                                 img_0, img_1, img_2, patch_id))
        self.conn.commit()
        self.stopConnection()
        return JSONResponse(None, 200)

    def deleteData(self, email, id):
        """ Удаление записи. Поиск записи по EMAIL пользователя и ID """
        self.makeConnection()
        self.cur.execute(DELETE_DATA_BY_EMAIL_AND_ID, (email, id))
        self.conn.commit()
        self.stopConnection()
        return JSONResponse(None, 200)
