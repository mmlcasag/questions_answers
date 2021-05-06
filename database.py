
from flask import g
import sqlite3

def connect_db():
    sql = sqlite3.connect('/home/mmlcasag/python/questions_answers/database/questions_answers.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def close_db():
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
