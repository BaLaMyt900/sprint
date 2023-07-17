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