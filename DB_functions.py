import psycopg2
from psycopg2 import Error
from config import FSTR_DB_NAME, FSTR_DB_PORT, FSTR_DB_LOGIN, FSTR_DB_PASS, FSTR_DB_HOST
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from Data_class import Data, ResponsePerevalModel, ResponsePerevalByEmail, ResponsePerevalByEmailList
from DB_Requests import *
from fastapi.responses import JSONResponse


class Db:
    """ Класс для работы с базой данных """

    def __init__(self):
        """ Создание таблиц в базе данных """

        try:
            self.makeConnection()
        except (Exception, Error):
            raise Error('Ошибка подключения к базе данных')

        """ Создание таблицы Users """
        self.cur.execute(ADD_USERS)

        """ Создание таблицы Coords """
        self.cur.execute(ADD_COORDS)

        """ Создание таблицы pereval_images """
        self.cur.execute(ADD_IMAGES)

        """ Создание таблицы pereval_added """
        self.cur.execute(ADD_DATA)

        self.stopConnection()

    def makeConnection(self):
        """ Функция создания соединения с базой данных"""
        try:
            self.conn = psycopg2.connect(dbname=FSTR_DB_NAME, user=FSTR_DB_LOGIN, password=FSTR_DB_PASS,
                                         host=FSTR_DB_HOST,
                                         port=FSTR_DB_PORT)
            self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            self.cur = self.conn.cursor()
        except (Exception, Error) as error:
            raise error

    def stopConnection(self):
        """ Функция разрыва соединения с базой данных """
        self.cur.close()
        self.conn.close()

    def submitData(self, data: Data):
        """ Принятие новых данных """

        try:
            self.makeConnection()
        except (Exception, Error) as error:
            return JSONResponse({'status': 500, 'message': f'Ошибка подключения к базе данных - {error}', 'id': None})

        # Добавление фотографий

        images_id = []
        if data.images.root:
            if len(data.images.root) > 3:
                return JSONResponse({'status': 500, 'message': 'Слишком много фотографий. Максимально 3.'})
            for image in data.images.root:
                self.cur.execute(INSERT_IMAGE,
                                 (image.title, image.data,))
                images_id.append(self.cur.fetchone())

        # Добавление координат

        self.cur.execute(INSERT_COORDS,
                         (data.coords.latitude, data.coords.longitude, data.coords.height,))
        coords_id = self.cur.fetchone()

        # Поиск или добавление пользователя

        self.cur.execute(SELECT_USER_BY_EMAIL, (data.user.email,))
        user_id = self.cur.fetchone()

        # Добавление информации в pereval_added

        if user_id:  # Если пользователь найдет, добавление с имеющимся ИД
            self.cur.execute(INSERT_DATA_RETURN_ID,
                             (data.beauty_title, data.title, data.other_titles,
                              data.connect, user_id,
                              coords_id))
            object_id = self.cur.fetchone()
        else:  # Иначе добавление пользователя а потом уже информации
            self.cur.execute(INSERT_USER_RETURN_ID,
                             (data.user.email, data.user.phone, data.user.fam, data.user.name, data.user.oct))
            user_id = self.cur.fetchone()
            self.cur.execute(INSERT_DATA_RETURN_ID,
                             (data.beauty_title, data.title, data.other_titles,
                              data.connect, user_id, coords_id))
            object_id = self.cur.fetchone()

        if images_id:
            for img_id, image_id in enumerate(images_id):
                self.cur.execute(UPDATE_DATA_ADD_IMAGE_BY_IMG_ID, (img_id, image_id, object_id))

        self.stopConnection()

        return JSONResponse({'status': 200, 'message': None, 'id': object_id})

    def getData(self, data_id: int):
        """ Функция получения данных из базы """
        self.makeConnection()
        self.cur.execute(SELECT_DATA_BY_ID_FOR_GET_REQUEST, (data_id,))
        data = self.cur.fetchone()
        self.stopConnection()
        if data:  # if для транформации memoryview из БД в bytea для модели
            return ResponsePerevalModel(**{key: data[i].tobytes() if isinstance(data[i], memoryview) else data[i]
                                           for i, key in enumerate(ResponsePerevalModel.model_fields.keys())})
        else:
            return JSONResponse({'status': 204, 'message': 'Данные не найдены.'})

    def _updatePhoto(self, img_id: int, old_title: str, old_data: bytes, new_title: str, new_data: bytes):
        """ Внутренний метод сравнения и обновления фотографий. """
        if all([img_id, any([old_title != new_title, old_data != new_data])]):
            self.cur.execute(UPDATE_PHOTO_FOR_PATCH, (new_title, new_data, img_id))
            return img_id
        elif not img_id:
            self.cur.execute(INSERT_IMAGE, (new_title, new_data))
            return self.cur.fetchone()

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
                return JSONResponse({'state': 0, 'message': 'Запрещено изменять провернные данные.'})
            elif any([oldData[1] != data.user.email, oldData[2] != data.user.name, oldData[3] != data.user.fam,
                      oldData[4] != data.user.oct, oldData[5] != data.user.phone]):
                """ Проверка на соответсвие данных пользователя. """
                return JSONResponse({'state': 0, 'message': 'Запрещено менять данные пользователя.'})
        else:
            """ Проверка нахождения данных по id """
            return JSONResponse({'state': 0, 'message': 'Данные не найдены.'})
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
        self.stopConnection()
        return JSONResponse({'state': 1, 'message': None})

    def getByEmail(self, email: str):
        """ Получение данных по email пользователя. """
        self.makeConnection()
        self.cur.execute(SELECT_USER_BY_EMAIL, (email,))
        user_id = self.cur.fetchone()
        if not user_id:
            """ Проверка нахождения пользователя """
            return JSONResponse({'status': 0, 'message': 'Пользователь не найден.'})
        self.cur.execute(SELECT_DATA_FOR_SEARCH_BY_USER_ID, (user_id,))
        data_list = self.cur.fetchall()
        self.stopConnection()
        if not data_list:
            """ Проверка наличия выходных данных """
            return JSONResponse({'status': 0, 'message': 'Данные не найдены.'})
        output_data = []
        for item in data_list:
            output_data.append({key: item[i].tobytes() if isinstance(item[i], memoryview) else item[i]
                                for i, key in enumerate(ResponsePerevalByEmail.model_fields.keys())})
        return JSONResponse({'status': 1, 'data': ResponsePerevalByEmailList(root=output_data).model_dump(mode='json')})
