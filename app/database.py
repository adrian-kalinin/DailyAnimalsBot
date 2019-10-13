import sqlite3


class DataBase:
    def __init__(self, name='users'):
        self.name = name
        self.conn = sqlite3.connect(name + '.sqlite')

    def __enter__(self):
        self.setup()
        return self

    def __exit__(self, ex_type, value, traceback):
        self.close()

    def setup(self):
        self.conn.execute(
            f'CREATE TABLE IF NOT EXISTS {self.name} ('
            'user_id INTEGER NOT NULL PRIMARY KEY UNIQUE,'
            'lang TEXT NOT NULL DEFAULT "en",'
            'cats INTEGER NOT NULL DEFAULT 0,'
            'dogs INTEGER NOT NULL DEFAULT 0);'
        )
        self.conn.commit()

    def get_users(self):
        result = self.conn.execute(f'SELECT user_id FROM {self.name}')
        return [x[0] for x in result]

    def get_cats(self):
        result = self.conn.execute(f'SELECT SUM(cats) FROM {self.name}')
        return result.fetchone()[0]

    def get_dogs(self):
        result = self.conn.execute(f'SELECT SUM(dogs) FROM {self.name}')
        return result.fetchone()[0]

    def add_user(self, user_id):
        if not self.check_user(user_id):
            stat = f'INSERT INTO {self.name} (user_id) VALUES (?)'
            self.conn.execute(stat, [user_id])
            self.conn.commit()

    def del_user(self, user_id):
        stat = f'DELETE FROM {self.name} WHERE user_id = (?)'
        if self.check_user(user_id):
            self.conn.execute(stat, [user_id])
            self.conn.commit()

    def check_user(self, user_id):
        stat = f'SELECT EXISTS(SELECT 1 FROM {self.name} WHERE user_id = (?));'
        result = self.conn.execute(stat, [user_id])
        return result.fetchone()[0]

    def get_users_amount(self):
        stat = f'SELECT Count(*) FROM {self.name}'
        result = self.conn.execute(stat)
        return result.fetchone()[0]

    def set(self, user_id, item, data):
        if self.check_user(user_id):
            stat = f'UPDATE {self.name} SET {item} = (?) WHERE user_id = (?)'
            self.conn.execute(stat, (data, user_id))
            self.conn.commit()

    def get(self, user_id, item):
        if self.check_user(user_id):
            stat = f'SELECT {item} FROM {self.name} WHERE user_id = (?)'
            result = self.conn.execute(stat, [user_id]).fetchone()
            return result[0]

    def close(self):
        self.conn.close()
