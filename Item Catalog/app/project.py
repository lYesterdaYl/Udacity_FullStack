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

@app.route('/catelog/<string:item_title>/edit', methods=['GET', 'POST'])
def edit_item(item_title):
    editedItem = session.query(Item).filter_by(title=item_title).one()
    categories = session.query(Category)
    if request.method == 'POST':
        if request.form['title']:
            editedItem.title = request.form['title']
            print(request.form['title'])
        if request.form['description']:
            editedItem.description = request.form['description']
            print(request.form['description'])
        if request.form['category']:
            editedItem.category = request.form['category']
            print(request.form['category'])
        print(editedItem.title)
        session.add(editedItem)
        session.commit()
        flash("menu item edited!")
        return redirect(url_for('index'))
    else:
        return render_template(
            'edit_item.html', item_title = item_title, item = editedItem, categories = categories)

@app.route('/catelog/<string:item_title>/delete', methods=['GET', 'POST'])
def delete_item(item_title):
    deletedItem = session.query(Item).filter_by(title=item_title).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash("menu item deleted!")
        return redirect(url_for('index'))
    else:
        return render_template(
            'delete_item.html', item=deletedItem)
    return "delete successful"

if __name__ == '__main__':
    app.secret_key = "secret_key"
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
