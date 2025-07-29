from flask import g
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from helpers.application import app

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

db.init_app(app)

# Legado.
DATABASE = 'censoescolar.db'

def getConnection():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = psycopg2.connect(user="postgres",
                                            password="123456",
                                            host="127.0.0.1",
                                            port="5434",
                                            database="censoescolar")
    return db

@app.teardown_appcontext
def closeConnection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()