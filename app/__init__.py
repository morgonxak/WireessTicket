from flask import Flask
from testDB import DBManager


db = DBManager('mydatabase.db')
app = Flask(__name__)
app.config['db'] = db
from app import views
