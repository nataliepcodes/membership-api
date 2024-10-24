from flask import g 
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

database = os.getenv('DATABASE')

def connect_db():
    sql = sqlite3.connect('')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db