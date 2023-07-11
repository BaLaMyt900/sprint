import psycopg2
from config import FSTR_DB_NAME, FSTR_DB_PORT, FSTR_DB_LOGIN, FSTR_DB_PASS, FSTR_DB_HOST
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import json

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
        self.cur = self.conn.cursor()

    @staticmethod
    def stopconnection(conn, cur):
        """ Функция разрыва соединения с базой данных """
        cur.close()
        conn.close()

    def submitdata(self, data: dict):
        """ Принятие новых данных """
        self.makeconnection()
        print(dict(data))
        print(data['title'])
        # Добавление фотографий
        images = data.images
        for image in images:
            self.cur.execute('''INSERT INTO pereval_images (title, img) VALUES (?,?) RETURNING id''',
                             (image['title'], image['data']))
            image = self.cur.fetchone()

        # Добавление координат
        self.cur.execute('''INSERT INTO Coords (latitude, longitude, height) VALUES (?, ?, ?) RETURNING id''',
                         (data['coords']['latitude'], data['coords']['longitude'], data['coords']['height']))
        coords_id = self.cur.fetchone()

        # Поиск или добавление пользователя
        self.cur.execute(f'''SELECT id FROM Users WHERE email ={data['user']['email']}''')
        user_id = self.cur.fetchone()

        if user_id:
            self.cur.execute(''' INSERT INTO pereval_added (beautyTitle, title, others_titles, connect, user
            images, coords) VALUES (?,?,?,?,?,?)''', (data['beauty_title'], data['title'], data['others_titles'],
                                                      data['connect'], user_id, images, coords_id))
