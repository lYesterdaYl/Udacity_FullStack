from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# engine = create_engine('sqlite:///restaurantmenu.db')
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

myFirstRestaurant = Restaurant(name="Pizza Palace")
mySecondRestaurant = Restaurant(name="KFC")

cheesepizza = MenuItem(name="Cheese Pizza", description="Make with XXX", course="Entree", price="$1.11", restaurant=myFirstRestaurant)
chickenpizza = MenuItem(name="Chicken Pizza", description="Make with XXX", course="Entree", price="$3.99", restaurant=myFirstRestaurant)
beefpizza = MenuItem(name="Beef Pizza", description="Make with XXX", course="Entree", price="$4.99", restaurant=myFirstRestaurant)
porkpizza = MenuItem(name="Pork Pizza", description="Make with XXX", course="Entree", price="$5.99", restaurant=myFirstRestaurant)
mushroompizza = MenuItem(name="Mushroom Pizza", description="Make with XXX", course="Entree", price="$6.99", restaurant=myFirstRestaurant)

session.add(myFirstRestaurant)
session.add(cheesepizza)
session.add(chickenpizza)
session.add(beefpizza)
session.add(porkpizza)
session.add(mushroompizza)

session.commit()

print(session.query(Restaurant).all())
print(session.query(MenuItem).all())