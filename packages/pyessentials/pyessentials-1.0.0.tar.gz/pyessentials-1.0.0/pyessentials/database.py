import sqlite3
import threading
import time

FETCH_NONE = 0
FETCH_ONE = 1
FETCH_ALL = 2

class QueryDB:
    def __init__(self, file):
        self.id = 0
        self.queue = {}
        self.file = file
        self.database = sqlite3.connect(self.file, check_same_thread = False)
        self.cursor = self.database.cursor()
        threading.Thread(target = self.thread).start()

    def thread(self):
        while True:
            while not self.queue:
                time.sleep(0.001)
            for key, value in self.queue.copy().items():
                if (not value['fetch_mode'] and value['result'] != -1) or (value['fetch_mode'] and value['result'] != -1 and value['fetched']):
                    del self.queue[key]
                    continue
                if value['result'] == -1:
                    if not value['data']:
                        self.cursor.execute(value['query'])
                    else:
                        self.cursor.execute(value['query'], value['data'])
                    if value['fetch_mode']:
                        if value['fetch_mode'] == FETCH_ONE:
                            self.queue[key]['result'] = self.cursor.fetchone()
                        elif value['fetch_mode'] == FETCH_ALL:
                            self.queue[key]['result'] = self.cursor.fetchall()
                    else:
                        self.queue[key]['result'] = tuple()
                    if value['save']:
                        self.database.commit()

    def execute(self, query, data = None, fetch_mode = FETCH_NONE, save = False):
        self.id += 1
        id_copy = self.id
        self.queue[id_copy] = {'query': query, 'fetch_mode': fetch_mode, 'data': data, 'save': save, 'result': -1, 'fetched': 0}
        if fetch_mode:
            while self.queue[id_copy]['result'] == -1:
                time.sleep(0.001)
            result = self.queue[id_copy]['result']
            self.queue[id_copy]['fetched'] = 1
            return result

class Database:
    def __init__(self, file):
        self.file = file
        self.database = QueryDB(file)

    def create(self, table, fields = []):
        query = 'CREATE TABLE IF NOT EXISTS ' + str(table)
        query += ' (' + ', '.join([field + ' text' for field in fields]) + ')'
        self.database.execute(query, save = True)

    def write(self, table, values = []):
        query = 'INSERT INTO ' + str(table) + ' VALUES'
        query += ' (' + ', '.join(['?'] * len(values)) + ')'
        self.database.execute(query, tuple(values), save = True)

    def read(self, table, condition = {}):
        query = 'SELECT * FROM ' + str(table)
        if condition:
            query += ' WHERE ' + ' and '.join([str(key) + '=?' for key in condition.keys()])
            response = self.database.execute(query, tuple(condition.values()), fetch_mode = FETCH_ALL)
        else:
            response = self.database.execute(query, fetch_mode = FETCH_ALL)
        generated = []
        for row in response:
            generated.append(tuple(row))
        return tuple(generated)

    def update(self, table, update = tuple(), condition = {}):
        query = 'UPDATE ' + str(table) + ' SET ' + str(update[0]) + '=?'
        if not condition:
            self.database.execute(query, tuple([str(update[1])]), save = True)
        else:
            query += ' WHERE ' + ' and '.join([str(key) + '=?' for key in condition.keys()])
            self.database.execute(query, tuple([str(update[1])] + list(condition.values())), save = True)

    def delete(self, table, condition = {}):
        query = 'DELETE FROM ' + str(table)
        if condition:
            query += ' WHERE ' + ' and '.join([str(key) + '=?' for key in condition.keys()])
            self.database.execute(query, tuple(condition.values()), save = True)
        else:
            self.database.execute(query, save = True)

    def drop(self, table):
        query = 'DROP TABLE ' + str(table)
        self.database.execute(query, save = True)