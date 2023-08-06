# Copyright © 2020 Noel Kaczmarek
from contextlib import closing

import mysql.connector
import psycopg2
import sqlite3
import uuid
import os


class PostgreSQLDatabase(object):
    def __init__(self, **kwargs):
        self.host = kwargs.get('host', 'localhost')
        self.port = kwargs.get('port', 5432)
        self.user = kwargs.get('user', 'root')
        self.password = kwargs.get('password', 'toor')
        self.database = kwargs.get('database', 'db')

    def connect(self):
        connection = psycopg2.connect(
          host=self.host,
          port=self.port,
          user=self.user,
          password=self.password,
          database=self.database
        )
        cursor = connection.cursor()
        return connection, cursor

    def query(self, sql, variables=None, **kwargs):
        try:
            connection, cursor = self.connect()
            cursor.execute(sql, variables)

            if kwargs.get('fetchone', False):
                result = cursor.fetchone()
            else:
                result = cursor.fetchall()
                
        except(Exception, psycopg2.Error) as e:
            print('Database error:', e)

        finally:
            if connection and cursor:
                cursor.close()
                connection.close()

                return result


class MySQLDatabase(object):
    def __init__(self, **kwargs):
        self.host = kwargs.get('host', 'localhost')
        self.user = kwargs.get('user', 'root')
        self.password = kwargs.get('password', 'toor')
        self.database = kwargs.get('database', 'db')

        self.connect()
        self.cursor = self.connection.cursor()

    def connect(self):
        self.connection = mysql.connector.connect(
          host=self.host,
          user=self.user,
          passwd=self.password,
          database=self.database
        )

    def get(self):
        return self.connection, self.cursor

    def query(self, sql, **kwargs):
        with closing(mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            database=self.database
        )) as con, closing(con.cursor()) as cur:
            cur.execute(sql)

            if kwargs.get('fetchone', False):
                return cur.fetchone()
            return cur.fetchall()


class SQLiteDatabase(object):
    def __init__(self, file):
        self.connection = sqlite3.connect(file)
        self.cursor = self.connection.cursor()
        self.file = file

    def connect(self):
        self.connection = sqlite3.connect(self.file)
        self.cursor = self.connection.cursor()

    def insert(self, values):
        command = 'INSERT INTO %s (user, firstname, lastname, username, password, gender, email, birthdate, adress, ' \
                  'rank) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s);' % (
                      values[0], values[1], values[2], values[3], values[4],
                      values[5], values[6], values[7], values[8])

        self.execute(command)
        self.commit()

    def get(self):
        self.connect()
        return self.connection, self.cursor

    def query(self, sql, **kwargs):
        with closing(sqlite3.connect(self.file)) as con, con,  \
                closing(con.cursor()) as cur:
            cur.execute(sql)
            if kwargs.get('fetchone', False):
                return cur.fetchone()
            return cur.fetchall()

    def execute(self, command):
        self.cursor.execute(command)

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()
