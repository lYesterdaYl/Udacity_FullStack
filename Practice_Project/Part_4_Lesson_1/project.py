from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
app = Flask(__name__)


# engine = create_engine('sqlite:///restaurantmenu.db?check_same_thread=False')
DIALCT = "mysql"
DRIVER = "pymysql"
USERNAME = "root"
PASSWORD = ""
HOST = "127.0.0.1"
PORT = "3306"
DATABASE = "test"
DB_URI="{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALCT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
engine = create_engine(DB_URI)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).first()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)


@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def new_Menu_Item(restaurant_id):
    if request.method == 'POST':
        new_item = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
        session.add(new_item)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)
    return "create successful"

@app.route('/restaurants/<int:restaurant_id>/edit')
def edit_Menu_Item(restaurant_id):
    return "edit successful"

@app.route('/restaurants/<int:restaurant_id>/delete')
def delete_Menu_Item(restaurant_id):
    return "delete successful"

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
