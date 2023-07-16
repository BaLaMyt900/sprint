import psycopg2
from config import FSTR_DB_NAME, FSTR_DB_PORT, FSTR_DB_LOGIN, FSTR_DB_PASS, FSTR_DB_HOST
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from Data_class import Data
from datetime import datetime


class Db:
    """ Класс для работы с базой данных """

    def __init__(self):
        """ Создание таблиц в базе данных """
        self.conn = psycopg2.connect(dbname=FSTR_DB_NAME, user=FSTR_DB_LOGIN, password=FSTR_DB_PASS, host=FSTR_DB_HOST,
                                     port=FSTR_DB_PORT)
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cur = self.conn.cursor()
        """ Создание таблицы Users """
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Users 
                        (
                            id serial PRIMARY KEY,
                            email text UNIQUE,
                            phone integer UNIQUE,
                            fam varchar(50) NOT NULL,
                            name varchar(50) NOT NULL,
                            oct varchar(50),
                            CONSTRAINT User_unique UNIQUE (id, email)
                        );
                        ''')

        """ Создание таблицы Coords """
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Coords
                        (
                            id serial PRIMARY KEY,
                            latitude float NOT NULL,
                            longitude float NOT NULL,
                            height integer NOT NULL
                        );""")

        """ Создание таблицы pereval_images """
        self.cur.execute('''CREATE TABLE IF NOT EXISTS pereval_images
                        (
                            id serial PRIMARY KEY,
                            title text,
                            date timestamp DEFAULT CURRENT_TIMESTAMP,
                            img bytea NOT NULL
                        );''')

        """ Создание таблицы pereval_added """
        self.cur.execute('''CREATE TABLE IF NOT EXISTS pereval_added
                        (
                            id serial PRIMARY KEY,
                            status text DEFAULT 'new',
                            beautyTitle text,
                            title text,
                            others_titles text,
                            connect text,
                            user_id int,
                            images int,
                            date_added timestamp DEFAULT CURRENT_TIMESTAMP,
                            coords int NOT NULL,
							CONSTRAINT user_pk FOREIGN KEY (user_id) REFERENCES Users(id),
                            CONSTRAINT coords_pk FOREIGN KEY (coords) REFERENCES Coords(id) ON DELETE CASCADE,
                            CONSTRAINT images_pk FOREIGN KEY (images) REFERENCES pereval_images(id) ON DELETE CASCADE
                        );''')
        self.cur.close()
        self.conn.close()

    def makeconnection(self):
        """ Функция создания соединения с базой данных"""
        self.conn = psycopg2.connect(dbname=FSTR_DB_NAME, user=FSTR_DB_LOGIN, password=FSTR_DB_PASS, host=FSTR_DB_HOST,
                                     port=FSTR_DB_PORT)
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cur = self.conn.cursor()

    def stopconnection(self):
        """ Функция разрыва соединения с базой данных """
        self.cur.close()
        self.conn.close()

    def submitdata(self, data: Data):
        """ Принятие новых данных """
        self.makeconnection()
        # Добавление фотографий TODO Асинхронный ввод фотографий в БД
        images_id = []
        for image in data.images.root:
            self.cur.execute('''INSERT INTO pereval_images (title, img) VALUES (%s, %s) RETURNING id''',
                             (image.title, image.data, ))
            images_id.append(self.cur.fetchone())

        # Добавление координат
        self.cur.execute('''INSERT INTO Coords (latitude, longitude, height) VALUES (%s, %s, %s) RETURNING id''',
                         (data.coords.latitude, data.coords.longitude, data.coords.height, ))
        coords_id = self.cur.fetchone()

        # # Поиск или добавление пользователя TODO Прокверка ния пользователя иили добавление в БД
        self.cur.execute(f'''SELECT id FROM Users WHERE email = %s''', (data.user.email, ))
        user_id = self.cur.fetchone()

        if user_id:
            self.cur.execute(''' INSERT INTO pereval_added (beautyTitle, title, others_titles, connect, user
            images, coords) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id''', (data.beauty_title, data.title, data.other_titles,
                                                                     data.connect, user_id, images_id,
                                                                     coords_id))
            return self.cur.fetchone()

        else:
            self.cur.execute(''' INSERT INTO Users (email, phone, fam, name, oct) VALUES (%s, %s, %s, %s, %s) RETURNING id''',
                             (data.user.email, data.user.phone, data.user.fam, data.user.name, data.user.oct))
            user_id = self.cur.fetchone()
            self.cur.execute(''' INSERT INTO pereval_added (beautyTitle, title, others_titles, connect, user_id,
                        images, coords) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id''',
                             (data.beauty_title, data.title, data.other_titles,
                              data.connect, user_id, images_id, coords_id))
            return self.cur.fetchone()

        # TODO асинхронная отправка работ с БД, сбор в единый ответ и ответ пользователю PROMISE
        # ПОИСК ФРЕЙМВОКОВ ДЛЯ РАБОТЫ С БД
