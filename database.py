from flask import g 
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

database = os.getenv('DATABASE')
# print(f"Database path: {database}")

def connect_db():
    sql = sqlite3.connect(database)
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db