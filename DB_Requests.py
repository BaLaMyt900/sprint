""" Файл с заготовленными запросами в базу данных. """


ADD_USERS = '''CREATE TABLE IF NOT EXISTS Users
                        (
                            id serial PRIMARY KEY,
                            email text UNIQUE,
                            phone integer UNIQUE,
                            fam varchar(50) NOT NULL,
                            name varchar(50) NOT NULL,
                            oct varchar(50),
                            CONSTRAINT User_unique UNIQUE (id, email)
                        );
                        '''
ADD_COORDS = """CREATE TABLE IF NOT EXISTS Coords
                        (
                            id serial PRIMARY KEY,
                            latitude float NOT NULL,
                            longitude float NOT NULL,
                            height integer NOT NULL
                        );"""
ADD_IMAGES = '''CREATE TABLE IF NOT EXISTS pereval_images
                        (
                            id serial PRIMARY KEY,
                            title text,
                            date timestamp DEFAULT CURRENT_TIMESTAMP,
                            img bytea NOT NULL
                        );'''
ADD_DATA = '''CREATE TABLE IF NOT EXISTS pereval_added
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
                        );'''
INSERT_IMAGE = '''INSERT INTO pereval_images (title, img) VALUES (%s, %s) RETURNING id'''
INSERT_COORDS = '''INSERT INTO Coords (latitude, longitude, height) VALUES (%s, %s, %s) RETURNING id'''
SELECT_USER_BY_EMAIL = '''SELECT id FROM Users WHERE email = %s'''
INSERT_DATA_RETURN_ID = ''' INSERT INTO pereval_added (beautyTitle, title, others_titles, connect, user_id,
            coords) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id'''
INSERT_USER_RETURN_ID = ''' INSERT INTO Users (email, phone, fam, name, oct) VALUES (%s, %s, %s, %s, %s) RETURNING id'''
UPDATE_DATA_ADD_IMAGE_BY_IMG_ID = ''' UPDATE pereval_added SET image_%s = %s WHERE id = %s'''
SELECT_DATA_BY_ID_FOR_GET_REQUEST = '''select status, u.email, u.fam, u.name, u.oct, u.phone, beautytitle,
                                       pereval_added.title, others_titles, connect, date_added,
                                       latitude, longitude, height, img_0.title, img_0.img, img_1.title,
                                       img_1.img, img_2.title, img_2.img
                                       from pereval_added
                                       join users u on u.id = pereval_added.user_id
                                       join coords on pereval_added.coords = coords.id
                                       LEFT JOIN pereval_images img_0 on img_0.id = pereval_added.image_0
                                       LEFT JOIN pereval_images img_1 on img_1.id = pereval_added.image_1
                                       LEFT JOIN pereval_images img_2 on img_2.id = pereval_added.image_2
                                       where pereval_added.id = %s;'''
SELECT_DATA_FOR_PATCH = '''SELECT status, u.email, u.name, u.fam, u.oct, u.phone,
                           coords, latitude, longitude, height, 
                           image_0, img_0.title, img_0.img,
                           image_1, img_1.title, img_1.img, 
                           image_2, img_2.title, img_2.img 
                           FROM pereval_added 
                           LEFT JOIN users u on u.id = pereval_added.user_id 
                           LEFT JOIN coords on pereval_added.coords = coords.id  
                           LEFT JOIN pereval_images img_0 on img_0.id = pereval_added.image_0
                           LEFT JOIN pereval_images img_1 on img_1.id = pereval_added.image_1
                           LEFT JOIN pereval_images img_2 on img_2.id = pereval_added.image_2
                           WHERE pereval_added.id = %s '''
UPDATE_DATA_FOR_PATCH = '''UPDATE pereval_added pa
                           SET beautytitle = %s, title = %s, others_titles = %s, connect = %s, image_0 = %s, 
                               image_1 = %s, image_2 = %s
                           WHERE id = %s'''
UPDATE_COORDS_FOR_PATCH = '''UPDATE coords
                             SET latitude = %s, longitude = %s, height = %s
                             WHERE id = %s'''
UPDATE_PHOTO_FOR_PATCH = '''UPDATE pereval_images
                            SET title = %s, img = %s
                            WHERE id = %s'''
