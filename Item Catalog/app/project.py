from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

app = Flask(__name__)

DIALCT = "mysql"
DRIVER = "pymysql"
USERNAME = "root"
PASSWORD = ""
HOST = "127.0.0.1"
PORT = "3306"
DATABASE = "item_catalog"
DB_URI="{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALCT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
engine = create_engine(DB_URI)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/index')
def index():
    categories = session.query(Category)
    items = session.query(Item)
    return render_template('index.html', categories=categories, items=items)

# @app.route('/catelog/<int:category_id>/')
@app.route('/catelog/<string:category_name>/items')
def show_category(category_name):
    categories = session.query(Category)
    category = session.query(Category).filter_by(name = category_name)
    items = session.query(Item).filter_by(category_id = category[0].id)
    return render_template('category.html',categories=categories,category=category, items=items)

@app.route('/item/<int:item_id>/')
def show_item(item_id):
    item = session.query(Item).filter_by(id = item_id)
    return render_template('item_description.html',item = item)

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
