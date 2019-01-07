from flask import Flask, render_template, request, redirect, \
    url_for, flash, jsonify, make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests

app = Flask(__name__)
CLIENT_ID = json.loads(open('client_secrets.json', 'r')
                       .read())['web']['client_id']
APPLICATION_NAME = "Item Catalog App"

# MySQL database information
# DIALCT = "mysql"
# DRIVER = "pymysql"
# USERNAME = "root"
# PASSWORD = ""
# HOST = "127.0.0.1"
# PORT = "3306"
# DATABASE = "item_catalog"
# DB_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8"\
#     .format(DIALCT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
# engine = create_engine(DB_URI)
engine = create_engine('sqlite:///restaurantmenu.db?check_same_thread=False')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showlogin():
    """
    render login button for google account users
    """
    state = ''.join([random.choice(string.ascii_uppercase + string.digits)
                     for i in range(30)])
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """
    login with google account
    """
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps(
            'Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    response = h.request(url, 'GET')
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    print(data)
    login_session['account_id'] = data['id']
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user = session.query(User).filter_by(account_id=data['id']).first()
    if user is None:
        new_user = User(account_id=data['id'],
                        email=data['email'],
                        name=data['name'],
                        given_name=data['given_name'],
                        account_link=data['link'],
                        picture_link=data['picture'],
                        )
        session.add(new_user)
        session.commit()

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;' \
              '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output


@app.route('/gdisconnect')
def gdisconnect():
    """
    logout
    """
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s'\
          % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("you have successfully logout")
        return redirect("/index")
        # return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return redirect("/index")
        # return response


@app.route('/')
@app.route('/index')
def index():
    """
    main page
    """
    categories = session.query(Category)
    items = session.query(Item)
    status = 1 if "access_token" in login_session else 0
    return render_template('index.html', categories=categories,
                           items=items, status=status)


@app.route('/item/<int:item_id>/JSON')
def show_item_JSON(item_id):
    items = session.query(Item).filter_by(id=item_id)
    return jsonify(Item=[i.serialize for i in items])


@app.route('/catelog/<string:category_name>/items/JSON')
def show_category_JSON(category_name):
    categories = session.query(Category)
    category = session.query(Category).filter_by(name=category_name)
    items = session.query(Item).filter_by(category_id=category[0].id)
    return jsonify(Item=[i.serialize for i in items])


@app.route('/catelog/JSON')
def show_all_JSON():
    """
    show all available items in JSON format
    """
    items = session.query(Item)
    return jsonify(Item=[i.serialize for i in items])

# show all available items for a specific category in JSON format


@app.route('/catelog/<string:category_name>/items')
def show_category(category_name):
    categories = session.query(Category)
    category = session.query(Category).filter_by(name=category_name)
    items = session.query(Item).filter_by(category_id=category[0].id)
    status = 1 if "access_token" in login_session else 0
    return render_template('category.html', categories=categories,
                           category=category, items=items, status=status)


@app.route('/item/<int:item_id>/')
def show_item(item_id):
    """
    show item in JSON format
    :param item_id:
    """
    item = session.query(Item).filter_by(id=item_id)
    status = 1 if "access_token" in login_session else 0
    user = session.query(User).filter_by(
        account_id=login_session['account_id']).first()
    return render_template('item_description.html', item=item,
                           status=status, user=user)


@app.route('/catelog/<string:item_title>/edit', methods=['GET', 'POST'])
def edit_item(item_title):
    """
    edit item information
    :param item_title:
    """
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(Item).filter_by(title=item_title).one()
    user = session.query(User).filter_by(
        account_id=login_session['account_id']).first()
    if editedItem.user_id != user.id:
        return redirect('/login')
    categories = session.query(Category)
    status = 1 if "access_token" in login_session else 0
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
            'edit_item.html', item_title=item_title, item=editedItem,
            categories=categories, status=status)


@app.route('/catelog/<string:item_title>/delete', methods=['GET', 'POST'])
def delete_item(item_title):
    """
    delete item from a category
    :param item_title:
    """
    if 'username' not in login_session:
        return redirect('/login')
    deletedItem = session.query(Item).filter_by(title=item_title).one()
    user = session.query(User).filter_by(
        account_id=login_session['account_id']).first()
    if deletedItem.user_id != user.id:
        return redirect('/login')
    status = 1 if "access_token" in login_session else 0
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash("menu item deleted!")
        return redirect(url_for('index'))
    else:
        return render_template(
            'delete_item.html', item=deletedItem, status=status)
    return "delete successful"


@app.route('/catelog/new_item', methods=['GET', 'POST'])
def new_item():
    """
    add new item under specific category.
    """
    if 'username' not in login_session:
        return redirect('/login')
    categories = session.query(Category)
    status = 1 if "access_token" in login_session else 0
    user = session.query(User).filter_by(
        account_id=login_session['account_id']).first()
    if request.method == 'POST':
        new_item = Item(title=request.form['title'],
                        description=request.form['description'],
                        category_id=request.form['category'],
                        user_id=user.id)
        session.add(new_item)
        session.commit()
        flash("new item created!")
        return redirect(url_for('index'))
    else:
        return render_template('new_item.html',
                               categories=categories, status=status)


@app.route('/catelog/new_category', methods=['GET', 'POST'])
def new_category():
    """
    add new category.
    """
    if 'username' not in login_session:
        return redirect('/login')
    status = 1 if "access_token" in login_session else 0
    if request.method == 'POST':
        new_category = Category(name=request.form['name'])
        session.add(new_category)
        session.commit()
        flash("new category created!")
        return redirect(url_for('index'))
    else:
        return render_template('new_category.html', status=status)


if __name__ == '__main__':
    app.secret_key = "secret_key"
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
