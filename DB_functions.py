import json

import psycopg2
from psycopg2 import Error
from config import FSTR_DB_NAME, FSTR_DB_PORT, FSTR_DB_LOGIN, FSTR_DB_PASS, FSTR_DB_HOST
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from Data_class import Data
from DB_Requests import *


class Db:
    """ Класс для работы с базой данных """

    def __init__(self):
        """ Создание таблиц в базе данных """

        try:
            self.makeconnection()
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
        self.cur.close()
        self.conn.close()

    def makeconnection(self):
        """ Функция создания соединения с базой данных"""
        try:
            self.conn = psycopg2.connect(dbname=FSTR_DB_NAME, user=FSTR_DB_LOGIN, password=FSTR_DB_PASS,
                                         host=FSTR_DB_HOST,
                                         port=FSTR_DB_PORT)
            self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            self.cur = self.conn.cursor()
        except (Exception, Error) as error:
            raise error

    def stopconnection(self):
        """ Функция разрыва соединения с базой данных """
        self.cur.close()
        self.conn.close()

    def submitData(self, data: Data):
        """ Принятие новых данных """

        try:
            self.makeconnection()
        except (Exception, Error) as error:
            return {'status': 500, 'message': f'Ошибка подключения к базе данных - {error}', 'id': None}

        # Добавление фотографий

        images_id = []
        if data.images.root:
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

        self.stopconnection()

        return {'status': 200, 'message': None, 'id': object_id}

    def getData(self, data_id: int):
        """ Функция получения данных из базы """
        self.makeconnection()
        self.cur.execute(SELECT_DATA_BY_ID_FOR_GET_REQUEST, (data_id,))
        response = self.cur.fetchone()
        self.stopconnection()
        return response


