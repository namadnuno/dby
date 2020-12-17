from logging import PlaceHolder
import mysql.connector
from mysql.connector.cursor import MySQLCursorPrepared

class DB():
    """
    This class will handle the DB connection and communications
    """

    host = 'localhost'
    user = 'root'
    password = ''
    db = ''

    conn = None
    cursor = None
    
    def __init__(self, host, user, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db

        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            db=db,
            charset= 'utf8',
        )
        self.cursor = self.conn.cursor(dictionary=True)


    
    def select(self, table, cols):
        statement = "SELECT * FROM " + table

        try:
            self.cursor.execute(statement)
        except:
            print("Erro:", self.cursor.statement)
            raise
        
        return self.cursor.fetchall()
    
    def insert(self, table, values):
        placeholders = ', '.join(['%s'] * len(values))
        columns = ', '.join(values.keys())
        statement = "INSERT INTO " + table + \
            "(%s) VALUES (%s)" % (columns, placeholders)
        try:
            self.cursor.execute(statement, (list(values.values())))
            self.conn.commit()
        except:
            print("Erro:", self.cursor.statement)
            raise
        
