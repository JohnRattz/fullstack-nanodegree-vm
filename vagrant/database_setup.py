import sys
import os
from sqlalchemy import create_engine
from sqlalchemy import \
    Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

database_engine_provider = 'sqlite'
database_name = 'restaurantmenu.db'
database_engine_string = database_engine_provider + ':///' + database_name

### Beginning Configuration Code ###
Base = declarative_base()


### Class Code ###
class Restaurant(Base):
    __tablename__ = 'restaurant'

    ### Mapper Code ###
    name = Column(
        String(80), nullable=False)
    id = Column(
        Integer, primary_key=True)


class MenuItem(Base):
    __tablename__ = 'menu_item'

    ### Mapper Code ###
    name = Column(
        String(80), nullable=False)
    id = Column(
        Integer, primary_key=True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(
        Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    # We added this serialize function to be able to
    # send JSON objects in a serializable format
    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'course': self.course,
        }


### Ending Configuration Code ###
engine = create_engine(database_engine_string)
Base.metadata.create_all(engine)
