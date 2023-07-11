import psycopg2
from config import dbname, FSTR_DB_PORT, FSTR_DB_LOGIN, FSTR_DB_PASS, FSTR_DB_HOST


def db_init():
    """ Создание таблиц в базе данных """
    conn = psycopg2.connect(dbname=dbname, user=FSTR_DB_LOGIN, password=FSTR_DB_PASS, host=FSTR_DB_HOST, port=FSTR_DB_PORT)
    cur = conn.cursor()

    """ Создание таблицы Users """
    cur.execute('''CREATE TABLE IF NOT EXISTS Users 
                (
                    id integer CONSTRAINT User_pk PRIMARY KEY,
                    email text,
                    phone integer,
                    fam varchar(50) NOT NULL,
                    name varchar(50) NOT NULL,
                    oct varchar(50),
                    CONSTRAINT User_unique UNIQUE (id, email)
                );
                ''')

    """ Создание таблицы Coords """
    cur.execute("""CREATE TABLE IF NOT EXISTS Coords
                (
                    id int UNIQUE PRIMARY KEY,
                    latitude float NOT NULL,
                    longitude float NOT NULL,
                    height integer NOT NULL
                );""")

    """ Создание таблицы pereval_images """
    cur.execute('''CREATE TABLE IF NOT EXISTS pereval_images
                (
                    id int UNIQUE PRIMARY KEY,
                    date timestamp DEFAULT CURRENT_TIMESTAMP,
                    img bytea NOT NULL
                );''')

    """ Создание таблицы pereval_added """
    cur.execute('''CREATE TABLE IF NOT EXISTS Pereval_added
                (
                    id integer NOT NULL UNIQUE PRIMARY KEY,
                    status text DEFAULT 'new',
                    beautyTitle text,
                    title text,
                    others_titles text,
                    connect text,
                    images int,
                    date_added timestamp DEFAULT CURRENT_TIMESTAMP,
                    coords int NOT NULL,
                    CONSTRAINT images_pk FOREIGN KEY (images) REFERENCES pereval_images(id) ON DELETE CASCADE
                );''')
    conn.close()


class Db:
    """ Класс для работы с базой данных """
    @staticmethod
    def submitdata(data):
        conn = psycopg2.connect(dbname=dbname, user=FSTR_DB_LOGIN, password=FSTR_DB_PASS, host=FSTR_DB_HOST,
                                port=FSTR_DB_PORT)
        cur = conn.cursor()

