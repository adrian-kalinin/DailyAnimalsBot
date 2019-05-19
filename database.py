import sqlite3
import json
import os


class DBHelper:
    def __init__(self, name='userdata.sqlite'):
        ''' Initialization '''
        self.name = name
        self.conn = sqlite3.connect(name)


    def __enter__(self):
        self.setup()
        return self


    def __exit__(self, type, value, traceback):
        self.close()


    def setup(self):
        ''' Setting up database '''
        stat = 'CREATE TABLE IF NOT EXISTS userdata (user_id INTEGER);'
        self.conn.execute(stat)
        self.conn.commit()


    def add_user(self, user_id):
        ''' Adding a new user by unique user_id '''
        if not self.check_user(user_id):
            stat = 'INSERT INTO userdata (user_id) VALUES (?)'
            args = (user_id, )
            self.conn.execute(stat, args)
            self.conn.commit()


    def del_user(self, user_id):
        ''' Deleting a user by unique user_id '''
        stat = 'DELETE FROM userdata WHERE user_id = (?)'
        args = (user_id, )
        if self.check_user(user_id):
            self.conn.execute(stat, args)
            self.conn.commit()


    def check_user(self, user_id):
        ''' Checking if user exists by unique user_id '''
        stat = 'SELECT user_id FROM userdata WHERE user_id = (?)'
        args = (user_id, )
        if self.conn.execute(stat, args).fetchone():
            return True


    def get_users(self):
        ''' Getting all user_id's '''
        result = self.conn.execute('SELECT user_id FROM userdata').fetchall()
        return [user[0] for user in result]


    def close(self):
        ''' Closing connection with database '''
        self.conn.close()


class StatCounter:
    def __init__(self):
        self.dogs = 0
        self.cats = 0
        self.load_data()


    def load_data(self):
        if 'stat.json' in os.listdir():
            with open('stat.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.dogs = data['dogs']
                self.cats = data['cats']
        else:
            self.save_data()


    def save_data(self):
        with open('stat.json', 'w', encoding='utf-8') as file:
            data = {'dogs': self.dogs, 'cats': self.cats}
            json.dump(data, file)


    def append_dog(self):
        self.dogs += 1


    def append_cat(self):
        self.cats += 1
