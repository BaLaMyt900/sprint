import psycopg2
from psycopg2 import Error
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
                            image_0 int,
                            image_1 int,
                            image_2 int,
                            date_added timestamp DEFAULT CURRENT_TIMESTAMP,
                            coords int NOT NULL,
							CONSTRAINT user_pk FOREIGN KEY (user_id) REFERENCES Users(id),
                            CONSTRAINT coords_pk FOREIGN KEY (coords) REFERENCES Coords(id) ON DELETE CASCADE,
                            CONSTRAINT image_0_fkey FOREIGN KEY (image_0) REFERENCES pereval_images(id) ON DELETE CASCADE,
                            CONSTRAINT image_1_fkey FOREIGN KEY (image_1) REFERENCES pereval_images(id) ON DELETE CASCADE,
                            CONSTRAINT image_2_fkey FOREIGN KEY (image_2) REFERENCES pereval_images(id) ON DELETE CASCADE
                        );''')
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
            return {'status': 500, 'message': f'Ошибка подключения к базе данных - {error}', 'id': None}

    def stopconnection(self):
        """ Функция разрыва соединения с базой данных """
        self.cur.close()
        self.conn.close()

    def submitdata(self, data: Data):
        """ Принятие новых данных """
        self.makeconnection()
        # Добавление фотографий
        images_id = []
        for image in data.images.root:
            self.cur.execute('''INSERT INTO pereval_images (title, img) VALUES (%s, %s) RETURNING id''',
                             (image.title, image.data,))
            images_id.append(self.cur.fetchone())

        # Добавление координат
        self.cur.execute('''INSERT INTO Coords (latitude, longitude, height) VALUES (%s, %s, %s) RETURNING id''',
                         (data.coords.latitude, data.coords.longitude, data.coords.height,))
        coords_id = self.cur.fetchone()

        # Поиск или добавление пользователя
        self.cur.execute(f'''SELECT id FROM Users WHERE email = %s''', (data.user.email,))
        user_id = self.cur.fetchone()

        # Добавление информации в pereval_added
        if user_id:  # Если пользователь найдет, добавление с имеющимся ИД
            self.cur.execute(''' INSERT INTO pereval_added (beautyTitle, title, others_titles, connect, user,
            coords) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id''',
                             (data.beauty_title, data.title, data.other_titles,
                              data.connect, user_id,
                              coords_id))
            object_id = self.cur.fetchone()
        else:  # Иначе добавление пользователя а потом уже информации
            self.cur.execute(
                ''' INSERT INTO Users (email, phone, fam, name, oct) VALUES (%s, %s, %s, %s, %s) RETURNING id''',
                (data.user.email, data.user.phone, data.user.fam, data.user.name, data.user.oct))
            user_id = self.cur.fetchone()
            self.cur.execute(''' INSERT INTO pereval_added (beautyTitle, title, others_titles, connect, user_id, 
            coords) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id''',
                             (data.beauty_title, data.title, data.other_titles,
                              data.connect, user_id, coords_id))
            object_id = self.cur.fetchone()

        for id, image_id in enumerate(images_id):
            self.cur.execute(f''' UPDATE pereval_added SET image_%s = %s WHERE id = %s''', (id, image_id, object_id))

        self.stopconnection()

        return {'status': 200, 'message': None, 'id': object_id}

