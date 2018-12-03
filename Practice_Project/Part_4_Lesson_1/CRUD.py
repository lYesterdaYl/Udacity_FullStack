from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

myFirstRestaurant = Restaurant(name="Pizza Palace")

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