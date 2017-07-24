from database_setup import Base, Restaurant, MenuItem, database_engine_string
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound


def display_veggie_burgers(veggie_burgers_list):
    print("All veggie burgers on the menu:")
    for veggie_burger_item in veggie_burgers_list:
        print(veggie_burger_item.id)
        print(veggie_burger_item.price)
        print(veggie_burger_item.restaurant.name)
        print("")


engine = create_engine(database_engine_string)
# Connect class definitions and their corresponding tables.
Base.metadata.bind = engine
# Link code executions and the engine.
DB_Session = sessionmaker(bind=engine)

session = DB_Session()

# TODO: Check if this entry already exists before adding?
my_first_restaurant = Restaurant(name="Pizza Palace")
session.add(my_first_restaurant)
session.commit()

# Add a menu item to the "Pizza Palace" menu.
cheese_pizza = MenuItem(
    name="Cheese Pizza",
    course="Entree",
    description="Made with all natural ingredients and fresh mozzarella",
    price="$8.99", restaurant=my_first_restaurant)
session.add(cheese_pizza)
session.query(MenuItem).all()

# Print the results of some queries.
first_result = session.query(Restaurant).first()
print("Name of first entry in the Restaurant table:", first_result.name)
print("All entries in the Restaurant table:")
items = session.query(Restaurant).all()
for item in items:
    print(item.name)
print("All entries in the MenuItems table:")
items = session.query(MenuItem).all()
for item in items:
    print(item.name)

# Add veggie burgers to the menu.
veggie_burgers = session.query(MenuItem).filter_by(name='Veggie Burger')

print("Veggie burgers on the menu:")
display_veggie_burgers(veggie_burgers)

# Query by id.
urban_veggie_burger = session.query(MenuItem).filter_by(id=9).one()
print("Initial Urban Veggie Burger price:", urban_veggie_burger.price)
# Change an single entry.
urban_veggie_burger.price = '$2.99'
print("Changed Urban Veggie Burger price:", urban_veggie_burger.price)
# Change multiple entries.
print("After changing veggie burger prices:")
display_veggie_burgers(veggie_burgers)

# Delete an entry from the database.
try:
    # Querying deleted data results in an exception.
    spinach_menu_item = session.query(MenuItem).filter_by(name='Spinach Ice Cream').one()
    print("Name of item being deleted:", spinach_menu_item.restaurant.name)
    session.delete(spinach_menu_item)
    session.commit()
except NoResultFound:
    print("Item deleted!")

